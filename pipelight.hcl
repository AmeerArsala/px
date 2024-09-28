pipelines = [
  {
    name = "fmt-n-lint"
    steps = [
      {
        name     = "format"
        commands = ["ruff format px"]
      },
      {
        name     = "lint"
        commands = ["ruff check px --fix"]
      }
    ]
    triggers = [{
      branches = ["main", "dev"]
      actions  = ["pre-commit", "pre-push"]
    }]
  }
]
