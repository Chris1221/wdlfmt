version 1.0

# What about here
struct Name {
  # coooooomment
    String myString
    # test comment
            # whoops
          # hi
    # comment
    Int myInt
}

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
    echo hi2; checking third line
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
    # this is also a comment but the indent is wrong
    #   Indented comments are conserved
  input {
    # asdfds
    File input_file
    # Another comment
    String hi=     "hi"
  }
  command <<<
    echo hi > hi.txt; echo hello
  >>> 

  output { 
    File hello = "hi.txt"
  }

    runtime { 
    docker: "gcr.io/docker:v1.0"
  }
}

workflow MyWorkflow { 
  # Test comment
  
  input { 
    File myfile = "hi"
    String yes
  }

  parameter_meta {
    myfile: "this is a file"
    yes: "this is a string"
  }

  String test = basename(myfile, ".bed")

  call Task2 as Task{
    input: 
      input_file = yes, 
      input2 = 5
  }

  # Comment sdlkfjasd

  call CalcMd5 {
    input: 
      input_file = myfile
  }

  output {
    File md5 = MD5.value
    File md52 = MD5.value2
  }


}