version 1.0


struct SampleInfo {
    String sampleId
    String libraryId
    Int readCount
    # Quality threshold for filtering
    Float qualThreshold
}

struct RunMetadata {
    String runId
    String platform
}

