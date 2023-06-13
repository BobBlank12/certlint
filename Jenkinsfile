pipeline {
  agent any
  stages {
    stage("Get Version Info") {
      steps {
        def versionFile = readFile('VERSION')
        // Extract the version information
        def version = versionFile.trim()
        // Print the version for verification
        sh "echo Version: ${version}"
        // set the version as an environment variable for later use
        env.VERSION = version
      }
    }
    stage("build") {
      def VERSION = versionFile.trim()
      steps {
        echo 'building the application...'
        sh 'echo ${VERSION}'
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