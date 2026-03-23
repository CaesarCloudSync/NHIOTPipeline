from NHIOTSub.subscriber import NHIOTSubscriber


if __name__ == "__main__":
    nhsub = NHIOTSubscriber()
    nhsub.monitor_workflow()