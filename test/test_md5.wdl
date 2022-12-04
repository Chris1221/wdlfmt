version 1.0

# Comment this is a comment

task CalcMd5 {
  # this is also a comment
  input {
    # asdfds
    File input_file
    # Another comment
    String hi=     "hi"
  }

  String test = basename(input_file, ".bed")

  command {
    # Comment
    /bin/my_md5sum2 ${input_file}
    echo hi ; echo this is a command too
  }
  
  # comment #3
  output {
    # Output comment
    File value = "md5sum.txt"
    File value2 = "blah.txt"
  }

 runtime {
    # Runtime comment
    # Runtime comment continued
    docker: "quay.io/briandoconnor/dockstore-tool-md5sum:1.0.2"
    cpu: 1
    memory: "512 MB"
 }
# WHat about there?
}
# And here?

task Task2 { 
    # this is also a comment
    #   Indented comments are conserved
  input {
    # asdfds
    File input_file
    # Another comment
    String hi=     "hi"
  }
}