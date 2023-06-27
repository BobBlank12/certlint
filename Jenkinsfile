pipeline {
  environment {
    DOCKERCREDS = credentials('dockerhub_id')
  }
  agent any
  stages {
    stage("Read the properties file") {
      steps {
        script {
          def props = readProperties file: 'PROPERTIES'
          env.VERSION = props.VERSION
          env.GCP_PROJECT = props.GCP_PROJECT
          env.GCP_LOCATION = props.GCP_LOCATION
          env.GCP_REPOSITORY = props.GCP_REPOSITORY
          env.IMAGE = props.IMAGE
          env.GCP_CLUSTER = props.GCP_CLUSTER
          env.DOCKERREGISTRY = props.DOCKERREGISTRY
        }
      }
    }
    stage("Build the Docker image and push to Docker Hub") {
      steps {
        echo 'Building the application...'
        // I had a problem here if my cluster was not 1.26, the uploads folder under website was getting deleted.
        script {
          //sh 'docker stop ${IMAGE}:${VERSION} || exit 0'
          sh 'docker rm -f ${IMAGE}:${VERSION} || exit 0'
          sh 'docker build --tag ${IMAGE}:${VERSION} .'
          sh 'docker tag ${IMAGE}:${VERSION} ${DOCKERREGISTRY}/${IMAGE}:${VERSION}'
          sh 'echo ${DOCKERCREDS_PSW} | docker login -u ${DOCKERCREDS_USR} --password-stdin'
          sh 'docker image push ${DOCKERREGISTRY}/${IMAGE}:${VERSION}'
        }
        echo "branch = ${BRANCH_NAME}"
      }
    }

    stage ('Add Latest tag when branch is main') {
        when {
            branch 'main'
        }
        steps {
          echo 'Add the Latest tag when on the main branch pipeline'
          script {
            sh 'docker tag ${IMAGE}:${VERSION} ${DOCKERREGISTRY}/${IMAGE}:latest'
            sh 'docker image push ${DOCKERREGISTRY}/${IMAGE}:latest'
          }
        }
    }

    stage("Test") {
      steps {
        echo 'testing the application...'
      }
    }
    stage("Tag and Push the image to GCP Artifact registry") {
      // I got the idea to use a SECRET FILE from here:
      //    https://stackoverflow.com/questions/45355007/how-to-authenticate-with-a-google-service-account-in-jenkins-pipeline
      // The official Google method using all of their plugins is here:
      //    https://cloud.google.com/kubernetes-engine/docs/archive/continuous-delivery-jenkins-kubernetes-engine
      steps {
        echo 'Pushing the application to GCP Artifact Registry'
        sh 'docker tag ${IMAGE}:${VERSION} ${GCP_LOCATION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPOSITORY}/${IMAGE}:${VERSION}'
        script {
          withCredentials([file(credentialsId: "${GCP_PROJECT}", variable: 'GC_KEY')]) {
            sh('gcloud auth activate-service-account --key-file=${GC_KEY}')
            sh('gcloud auth configure-docker ${GCP_LOCATION}-docker.pkg.dev')
            //sh('gcloud artifacts docker images delete --quiet ${GCP_LOCATION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPOSITORY}/${IMAGE}:${VERSION} --delete-tags || exit 0')
            sh('docker push ${GCP_LOCATION}-docker.pkg.dev/${GCP_PROJECT}/${GCP_REPOSITORY}/${IMAGE}:${VERSION}')
          }
        }
      }
    }
    stage("DELETE and re-deploy to GKE"){
      steps {
        echo 'Deploying the container to GKE'
        script {
          withCredentials([file(credentialsId: "${GCP_PROJECT}", variable: 'GC_KEY')]) {
            sh('gcloud auth activate-service-account --key-file=${GC_KEY}')
            sh('gcloud container clusters get-credentials ${GCP_CLUSTER}-${BRANCH_NAME} --zone=${GCP_LOCATION}-c --project=${GCP_PROJECT}')
            sh('kubectl delete deployment ${IMAGE} || exit 0')
            // Use sed to replace the $VERSION placeholder in the K8S application manifest file... chicken and egg problem.
            // most people would use a build hash here as an option... but still chicken and egg problem.
            //sh('sed "s/\\$VERSION/${VERSION}/" ${IMAGE}-application.yml')
            sh('sed "s/\\$VERSION/${VERSION}/" ${IMAGE}-application.yml | kubectl apply -f -')
            sh('kubectl apply -f ${IMAGE}-service.yml')
          }
        }
      }
    }
  }
}