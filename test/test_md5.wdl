version 1.0

task CalcMd5 {
  input {
    File input_file
  }

  command {
    /bin/my_md5sum ${input_file}
  }

 output {
    File value = "md5sum.txt"
    File value2 = "blah.txt"
 }

 runtime {
   docker: "quay.io/briandoconnor/dockstore-tool-md5sum:1.0.2"
   cpu: 1
   memory: "512 MB"
 }
}
