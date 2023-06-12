pipeline {
  agent any
  stages {
    stage("build") {
      steps {
        echo 'building the application...'
        sh 'docker stop certlint || exit 0'
      }
    }
    stage("test") {
      steps {
        echo 'testing the application...'
      }
    }
    stage("deploy") {
      steps {
        echo 'deploying the application...'
      }
    }
  }
}