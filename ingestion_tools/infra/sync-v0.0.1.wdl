version 1.0

task cryoet_data_sync_workflow {
    input {
        String docker_image_id
        String aws_region
        String input_path
        String input_bucket
        String output_bucket
        String output_path
        String flags
    }

    command <<<
        set -euxo pipefail
        export PYTHONUNBUFFERED=1
        python --version 1>&2
        ls -l 1>&2
        pwd 1>&2
        cd /usr/src/app/ingestion_tools/scripts
        aws s3 sync ~{flags} ~{input_bucket}~{input_path} ~{output_bucket}~{output_path} ~{flags} 1>&2
    >>>

    runtime {
        docker: docker_image_id
    }
}

workflow cryoet_data_sync {
    input {
        String docker_image_id = "cryoet_data_ingestion:latest"
        String aws_region = "us-west-2"
        String input_bucket = "cryoet-data-portal-staging"
        String input_path
        String output_bucket = "cryoet-data-portal-public"
        String output_path
        String flags
    }

    call cryoet_data_sync_workflow {
        input:
        docker_image_id = docker_image_id,
        aws_region = aws_region,
        input_bucket = input_bucket,
        input_path = input_path,
        output_bucket = output_bucket,
        output_path = output_path,
        flags = flags
    }

    output {
        File log = "output.txt"
    }
}
