# Problematic cases

import pytest
from tempfile import NamedTemporaryFile
import subprocess
import wdlfmt


@pytest.fixture
def common_error():
    return """
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

        command {
            bash -c '
            set  -e -o pipefail
            echo        "~{md5}  ~{file}" | md5sum -c
            '
        }

        runtime {
            docker: dockerImage
            memory: memory
        }
    }"""


@pytest.fixture
def unicycler():
    return """
    version 1.0

    # Copyright (c) 2017 Leiden University Medical Center
    #
    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:
    #
    # The above copyright notice and this permission notice shall be included in
    # all copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    # SOFTWARE.

    task Unicycler {
        input {
        String out
    }

    command <<<
        set -e -o pipefail
        mkdir -p ~{out}
        ~{preCommand}
        unicycler \\
        ~{"--short1 " + short1} \\
        ~{"--short2 " + short2} \\
        ~{"--unpaired " + unpaired} \\
        ~{"--long " + long} \\
        --out ~{out} \\
        ~{"--min_fasta_length " + minFastaLength} \\
        ~{"--keep " + keep } \\
        ~{true="--vcf" false="" vcf } \\
        ~{"--threads " + threads } \\
        ~{"--mode " + mode } \\
        ~{"--min_bridge_qual " + minBridgeQual } \\
        ~{"--linear_seqs " + linearSeqs } \\
        ~{"--spades_path " + spadesPath } \\
        ~{true="--no_correct" false="" noCorrect } \\
        ~{"--min_kmer_frac " + minKmerFrac } \\
        ~{"--max_kmer_frac " + maxKmerFrac } \\
        ~{"--kmer_count " + kmerCount } \\
        ~{"--depth_filter " + depthFilter } \\
        ~{true="--no_miniasm" false="" noMiniasm } \\
        ~{"--racon_path " + raconPath } \\
        ~{"--existing_long_read_assembly " + existingLongReadAssembly } \\
        ~{true="--no_rotate" false="" noRotate } \\
        ~{"--start_genes " + startGenes } \\
        ~{"--start_gene_id " + startGeneId } \\
        ~{"--start_gene_cov " + startGeneCov } \\
        ~{"--makeblastdb_path " + makeblastdbPath } \\
        ~{"--tblastn_path " + tblastnPath } \\
        ~{true="--no_pilon" false="" noPilon } \\
        ~{"--bowtie2_path " + bowtie2Path } \\
        ~{"--bowtie2_build_path " + bowtie2buildPath } \\
        ~{"--samtools_path " + samtoolsPath } \\
        ~{"--pilon_path " + pilonPath } \\
        ~{"--java_path " + javaPath } \\
        ~{"--min_polish_size " + minPolishSize } \\
        ~{"--bcftools_path " + bcftoolsPath } \\
        ~{"--min_component_size " + minComponentSize } \\
        ~{"--min_dead_end_size " + minDeadEndSize } \\
        ~{"--contamination " + contamination } \\
        ~{"--scores " + scores } \\
        ~{"--low_score " + lowScore }
    >>>

    output {
        File assemblyFasta = out + "/assembly.fasta"
        File assemblyGfa = out + "/assembly.gfa"
        File log = out + "/unicycler.log"
    }

    runtime {
        cpu: threads
        memory: memory
    }
}
"""


@pytest.fixture
def md5():
    """This one works on the command line but not in python...?"""
    return """
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

        command {
            bash -c '
            set -e -o pipefail
            echo "~{md5}  ~{file}" | md5sum -c
            '
        }

        runtime {
            docker: dockerImage
            memory: memory
        }
    }
    """


def test_string(common_error, unicycler, md5):
    cases = [common_error, unicycler, md5]
    for case in cases:
        wdlfmt.format_wdl_str(common_error)


def test_cases(common_error, unicycler, md5):
    cases = [unicycler, common_error, md5]
    for case in cases:
        with NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(case.encode())
            assert (
                subprocess.run(
                    ["/Users/ccole/miniconda3/bin/wdlfmt", tmpfile.name], shell=True
                ).returncode
                == 0
            )
