pipeline {
  agent any
  environment {
    //VERSION = "1.0.0"
  }
  stages {
    stage("Read properties file") {
      steps {
        script {
          def props = readProperties file: 'VERSION'
          env.VERSION = props.VERSION
        }
        echo "The VERSION is $VERSION"
      }
    }
    stage("build") {
      steps {
        echo 'building the application...'
        sh 'docker stop certlint || exit 0'
        sh 'docker rm certlint || exit 0'
        sh 'rm -rf ./website/uploads/* || exit 0'
        sh 'echo VERSION=${VERSION}'
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