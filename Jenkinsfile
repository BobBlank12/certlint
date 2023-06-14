pipeline {
  agent any
  stages {
    stage("Read the properties file") {
      steps {
        script {
          def props = readProperties file: 'PROPERTIES'
          env.VERSION = props.VERSION
        }
      }
    }
    stage("Build the Docker image") {
      steps {
        echo 'Building the application...'
        sh 'pwd'
        sh 'ls -la website'
        sh 'ls -la website/uploads'
        sh 'docker stop certlint || exit 0'
        sh 'docker rm certlint || exit 0'
        sh 'docker build --tag certlint:${VERSION} .'
      }
    }
    stage("test") {
      steps {
        echo 'testing the application...'
      }
    }
    stage("Tag and Push the image to GCP Artifact registry") {
      // I got the idea to use a SECRET FILE from here:
      //  https://stackoverflow.com/questions/45355007/how-to-authenticate-with-a-google-service-account-in-jenkins-pipeline
      steps {
        echo 'Pushing the application to GCP Artifact Registry'
        sh 'docker tag certlint:${VERSION} us-central1-docker.pkg.dev/mygcp-385621/webapp/certlint:${VERSION}'
        script {
          withCredentials([file(credentialsId: 'mygcp-385621', variable: 'GC_KEY')]) {
            sh('gcloud auth activate-service-account --key-file=${GC_KEY}')
            sh('gcloud auth configure-docker us-central1-docker.pkg.dev')
            sh('docker push us-central1-docker.pkg.dev/mygcp-385621/webapp/certlint:${VERSION}')
          }
        }
      }
    }
    stage("DELETE and re-deploy to GKE"){
      steps {
        echo 'Deploying the container to GKE'
        script {
          withCredentials([file(credentialsId: 'mygcp-385621', variable: 'GC_KEY')]) {
            sh('gcloud auth activate-service-account --key-file=${GC_KEY}')
            sh('gcloud container clusters get-credentials gcp-lab-gke --zone=us-central1-c --project=mygcp-385621')
            sh('kubectl delete -f certlint-gcp-k8s.yml || exit 0')
            sh('kubectl apply -f certlint-gcp-k8s.yml')
          }
        }
      }
    }
  }
}