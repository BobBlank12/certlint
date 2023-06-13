pipeline {
  agent any
  stages {
    stage("build") {
      def versionFile = readFile('VERSION')
      def VERSION = versionFile.trim()
      steps {
        echo 'building the application...'
        sh 'echo $VERSION'
        sh 'docker stop certlint || exit 0'
        sh 'docker rm certlint || exit 0'
        sh 'rm -rf ./website/uploads/* || exit 0'
        sh 'docker build --tag certlint .'
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