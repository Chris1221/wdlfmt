version 1.0


# This task will fail if the MD5sum doesn't match the file.
task CheckFileMD5 {
    input {
        File file
        String md5
        # By default cromwell expects /bin/bash to be present in the container.
        # The 'bash' container does not fill this requirement. (It is in /usr/local/bin/bash)
        # Use a stable version of debian:stretch-slim for this. (Smaller than ubuntu)
        String memory = "1GiB"
        String dockerImage = "debian@sha256:f05c05a218b7a4a5fe979045b1c8e2a9ec3524e5611ebfdd0ef5b8040f9008fa"
    }
    
    command <<<
        bash -c '
        set -e -o pipefail
        echo "~{md5}  ~{file}" | md5sum -c
        '
    >>>
    
    runtime {
        docker: dockerImage
        memory: memory
    }
    
}

