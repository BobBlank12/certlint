pipeline {
  agent any
  stages {
    stage("build") {
      steps {
        echo 'building the application...'
        sh 'docker stop certlint'
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