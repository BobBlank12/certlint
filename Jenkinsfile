pipeline {
  agent any
  environment {
    VERSION = "1.0.0"
  }
  stages {
    stage("build") {
      def VERSION = versionFile.trim()
      steps {
        echo 'building the application...'
        sh 'docker stop certlint || exit 0'
        sh 'docker rm certlint || exit 0'
        sh 'rm -rf ./website/uploads/* || exit 0'
        sh 'docker build --tag certlint:${VERSION} .'
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