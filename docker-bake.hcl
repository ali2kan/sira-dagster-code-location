group "default" {
  targets = ["dagster-pipeline"]
}

target "dagster-pipeline" {
  context = "."
  platforms = ["linux/amd64", "linux/arm64"]
  tags = [
    "ghcr.io/ali2kan/sira-dagster-standard-pipeline:multiarch",
    "ghcr.io/ali2kan/sira-dagster-standard-pipeline:latest"
  ]
  cache-from = ["type=registry,ref=ghcr.io/ali2kan/sira-dagster-standard-pipeline:buildcache"]
  cache-to = ["type=registry,ref=ghcr.io/ali2kan/sira-dagster-standard-pipeline:buildcache,mode=max"]
  args = {
    BUILDKIT_INLINE_CACHE = "1"
  }
}
