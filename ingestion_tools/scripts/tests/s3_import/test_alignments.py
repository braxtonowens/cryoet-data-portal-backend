import json
from os.path import basename
from typing import Callable

import pandas as pd
import pytest
from importers.alignment import AlignmentImporter
from importers.base_importer import BaseImporter
from importers.dataset import DatasetImporter
from importers.deposition import DepositionImporter
from importers.run import RunImporter
from mypy_boto3_s3 import S3Client
from standardize_dirs import IMPORTERS

from common.config import DepositionImportConfig
from common.fs import FileSystemApi
from tests.s3_import.util import get_data_from_s3, list_dir


def get_parents(config: DepositionImportConfig) -> dict[str, BaseImporter]:
    depositions = list(DepositionImporter.finder(config))
    datasets = list(DatasetImporter.finder(config, deposition=depositions[0]))
    runs = list(RunImporter.finder(config, dataset=datasets[0]))
    return {
        "deposition": depositions[0],
        "dataset": datasets[0],
        "run": runs[0],
    }


@pytest.fixture
def input_bucket() -> str:
    return "test-public-bucket"


@pytest.fixture
def add_alignment_metadata(s3_client: S3Client, test_output_bucket: str) -> Callable[[str, int], None]:
    def _add_alignment_metadata(prefix: str, deposition_id: int) -> None:
        body = json.dumps({"deposition_id": deposition_id}).encode("utf-8")
        s3_client.put_object(Bucket=test_output_bucket, Key=f"{prefix}100-alignment_metadata.json", Body=body)

    return _add_alignment_metadata


@pytest.fixture
def validate_dataframe(
    input_bucket: str,
    test_output_bucket: str,
    s3_client: S3Client,
) -> Callable[[str, str, int], None]:
    def get_data_frame(bucket_name: str, path: str) -> pd.DataFrame:
        body = get_data_from_s3(s3_client, bucket_name, path)
        return pd.read_csv(body, sep=r"\s+")

    def validate(prefix: str, filename: str, id_prefix: int) -> None:
        alignment_files = {basename(item) for item in list_dir(s3_client, test_output_bucket, prefix)}
        assert f"{id_prefix}-{filename}" in alignment_files
        actual = get_data_frame(input_bucket, f"input_bucket/10001_input/alignments/{filename}")
        expected = get_data_frame(test_output_bucket, f"{prefix}{id_prefix}-{filename}")
        assert actual.equals(expected)

    return validate


@pytest.fixture
def validate_metadata(s3_client: S3Client, test_output_bucket: str) -> Callable[[dict, str, int], None]:
    def validate(expected: dict, prefix: str, identifier: int) -> None:
        key = f"{prefix}{identifier}-alignment_metadata.json"
        actual = json.loads(s3_client.get_object(Bucket=test_output_bucket, Key=key)["Body"].read())
        for key in expected:
            assert actual[key] == expected[key], f"Key {key} does not match"

    return validate


@pytest.fixture
def create_config(
    s3_fs: FileSystemApi,
    test_output_bucket: str,
    input_bucket: str,
) -> Callable[[str], DepositionImportConfig]:
    def _create(path: str) -> DepositionImportConfig:
        output_path = f"{test_output_bucket}/output"
        import_config = f"tests/fixtures/{path}"
        return DepositionImportConfig(s3_fs, import_config, output_path, input_bucket, IMPORTERS)

    return _create


@pytest.mark.parametrize(
    "deposition_id, id_prefix",
    [
        (None, 100),  # No alignment metadata exists
        (100001, 101),  # alignment metadata exists for a different deposition
        (10301, 100),  # alignment metadata exists for the same deposition as test
    ],
)
def test_alignment_import_item(
    create_config: Callable[[str], DepositionImportConfig],
    add_alignment_metadata: Callable[[str, int], None],
    validate_dataframe: Callable[[str, str, int], None],
    validate_metadata: Callable[[dict, str, int], None],
    test_output_bucket: str,
    deposition_id: int,
    id_prefix: int,
) -> None:
    config = create_config("dataset1.yaml")
    parents = get_parents(config)
    dataset_name = parents.get("dataset").name
    run_name = parents.get("run").name
    prefix = f"output/{dataset_name}/{run_name}/Alignments/"
    if deposition_id:
        add_alignment_metadata(prefix, deposition_id)

    alignments = list(AlignmentImporter.finder(config, **parents))
    for alignment in alignments:
        alignment.import_item()
        alignment.import_metadata()

    validate_dataframe(prefix, "TS_run1.xf", id_prefix)
    validate_dataframe(prefix, "TS_run1.tlt", id_prefix)
    validate_dataframe(prefix, "TS_run1.xtilt", id_prefix)

    expected = {
        "affine_transformation_matrix": [[2, 0, 0, 0], [0, 3, 0, 0], [0, 4, 1, 0], [0, 0, 0, 5]],
        "alignment_path": f"{test_output_bucket}/{prefix}{id_prefix}-TS_run1.xf",
        "alignment_type": "LOCAL",
        "deposition_id": "10301",
        "is_canonical": True,
        "per_section_alignment_parameters": [
            {
                "z_index": 0,
                "in_plane_rotation": [0.029, 1.0, -1.0, 0.029],
                "x_offset": 55.43,
                "y_offset": 25.56,
                "tilt_angle": -5,
                "volume_x_rotation": 0.23,
            },
            {
                "z_index": 1,
                "in_plane_rotation": [0.029, 1.0, -1.0, 0.029],
                "x_offset": -75.84,
                "y_offset": 55.1,
                "tilt_angle": 0,
                "volume_x_rotation": 2.12,
            },
            {
                "z_index": 2,
                "in_plane_rotation": [0.029, 1.0, -1.0, 0.029],
                "x_offset": -93.8,
                "y_offset": 77.79,
                "tilt_angle": 5,
                "volume_x_rotation": 1.97,
            },
        ],
        "tilt_offset": -0.3,
        "tilt_path": f"{test_output_bucket}/{prefix}{id_prefix}-TS_run1.tlt",
        "tiltx_path": f"{test_output_bucket}/{prefix}{id_prefix}-TS_run1.xtilt",
        "volume_dimension": {"x": 6, "y": 8, "z": 10},
        "volume_offset": {"x": -1, "y": 2, "z": -3},
        "x_rotation_offset": -2.3,
    }
    validate_metadata(expected, prefix, id_prefix)


def test_default_alignment_import_with_tomograms(
    create_config: Callable[[str], DepositionImportConfig],
    s3_client: S3Client,
    test_output_bucket: str,
    validate_metadata: Callable[[dict, str, int], None],
) -> None:
    config = create_config("alignments/alignment1.yaml")
    parents = get_parents(config)

    alignments = list(AlignmentImporter.finder(config, **parents))
    for alignment in alignments:
        alignment.import_item()
        alignment.import_metadata()

    dataset_name = parents.get("dataset").name
    run_name = parents.get("run").name
    prefix = f"output/{dataset_name}/{run_name}/Alignments/"
    alignment_files = [
        basename(item) for item in list_dir(s3_client, test_output_bucket, prefix) if not item.endswith(".json")
    ]
    assert alignment_files == []
    expected = {
        "affine_transformation_matrix": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        "alignment_path": None,
        "alignment_type": "GLOBAL",
        "deposition_id": "10301",
        "is_canonical": False,
        "per_section_alignment_parameters": [],
        "tilt_offset": 0,
        "tilt_path": None,
        "tiltx_path": None,
        "volume_dimension": {"x": 6, "y": 8, "z": 10},
        "volume_offset": {"x": 0, "y": 0, "z": 0},
        "x_rotation_offset": 0,
    }
    validate_metadata(expected, prefix, 100)


def test_default_alignment_import_without_tomograms(
    create_config: Callable[[str], DepositionImportConfig],
    s3_client: S3Client,
    test_output_bucket: str,
) -> None:
    config = create_config("alignments/alignment2.yaml")
    parents = get_parents(config)

    alignments = list(AlignmentImporter.finder(config, **parents))
    for alignment in alignments:
        alignment.import_item()
        alignment.import_metadata()

    dataset_name = parents.get("dataset").name
    run_name = parents.get("run").name
    prefix = f"output/{dataset_name}/{run_name}/Alignments/"
    alignment_files = [basename(item) for item in list_dir(s3_client, test_output_bucket, prefix)]
    assert alignment_files == []


def test_custom_alignment_import_without_tomograms(
    create_config: Callable[[str], DepositionImportConfig],
    s3_client: S3Client,
    test_output_bucket: str,
    validate_dataframe: Callable[[str, str, int], None],
    validate_metadata: Callable[[dict, str, int], None],
) -> None:
    config = create_config("alignments/alignment3.yaml")
    parents = get_parents(config)

    alignments = list(AlignmentImporter.finder(config, **parents))
    for alignment in alignments:
        alignment.import_item()
        alignment.import_metadata()

    dataset_name = parents.get("dataset").name
    run_name = parents.get("run").name
    prefix = f"output/{dataset_name}/{run_name}/Alignments/"
    alignment_files = [basename(item) for item in list_dir(s3_client, test_output_bucket, prefix)]
    assert alignment_files == []


def test_custom_alignment_with_dimensions_import_without_tomograms(
    create_config: Callable[[str], DepositionImportConfig],
    test_output_bucket: str,
    validate_dataframe: Callable[[str, str, int], None],
    validate_metadata: Callable[[dict, str, int], None],
) -> None:
    config = create_config("alignments/alignment4.yaml")
    parents = get_parents(config)

    alignments = list(AlignmentImporter.finder(config, **parents))
    for alignment in alignments:
        alignment.import_item()
        alignment.import_metadata()

    dataset_name = parents.get("dataset").name
    run_name = parents.get("run").name
    prefix = f"output/{dataset_name}/{run_name}/Alignments/"
    id_prefix = 100

    validate_dataframe(prefix, "TS_run1.xf", id_prefix)
    expected = {
        "affine_transformation_matrix": [[2, 0, 0, 0], [0, 3, 0, 0], [0, 4, 1, 0], [0, 0, 0, 5]],
        "alignment_path": f"{test_output_bucket}/{prefix}{id_prefix}-TS_run1.xf",
        "alignment_type": "LOCAL",
        "deposition_id": "10301",
        "is_canonical": True,
        "per_section_alignment_parameters": [
            {
                "z_index": 0,
                "in_plane_rotation": [0.029, 1.0, -1.0, 0.029],
                "x_offset": 55.43,
                "y_offset": 25.56,
                "tilt_angle": None,
                "volume_x_rotation": 0,
            },
            {
                "z_index": 1,
                "in_plane_rotation": [0.029, 1.0, -1.0, 0.029],
                "x_offset": -75.84,
                "y_offset": 55.1,
                "tilt_angle": None,
                "volume_x_rotation": 0,
            },
            {
                "z_index": 2,
                "in_plane_rotation": [0.029, 1.0, -1.0, 0.029],
                "x_offset": -93.8,
                "y_offset": 77.79,
                "tilt_angle": None,
                "volume_x_rotation": 0,
            },
        ],
        "tilt_offset": -0.3,
        "tilt_path": None,
        "tiltx_path": None,
        "volume_dimension": {"x": 6, "y": 8, "z": 10},
        "volume_offset": {"x": -1, "y": 2, "z": -3},
        "x_rotation_offset": -2.3,
    }
    validate_metadata(expected, prefix, id_prefix)