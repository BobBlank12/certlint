pipeline {
  agent any
  stages {
    stage("Read properties file") {
      steps {
        script {
          def props = readProperties file: 'VERSION'
          env.VERSION = props.VERSION
        }
      }
    }
    stage("build") {
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
        sh 'docker tag certlint:${VERSION} us-central1-docker.pkg.dev/mygcp-385621/webapp/certlint:${VERSION}'
        sh 'docker push us-central1-docker.pkg.dev/mygcp-385621/webapp/certlint:${VERSION}'
      }
    }
  }
}