import torch

from LabelSeg.models.labelseg import LabelSeg


def get_model(checkpoint_file, kwargs={}):
    """ Get the model from a checkpoint. """

    # Load the model's hyper and actual params from a saved checkpoint
    try:
        checkpoint = torch.load(checkpoint_file, weights_only=False)
    except RuntimeError:
        # If the model was saved on a GPU and is being loaded on a CPU
        # we need to specify map_location=torch.device('cpu')
        checkpoint = torch.load(
            checkpoint_file, map_location=torch.device('cpu'),
            weights_only=False)

    # The model's class is saved in hparams
    models = {
        # Add other architectures here
        'LabelSeg': LabelSeg,
    }

    hyper_parameters = checkpoint["hyper_parameters"]

    # Load it from the checkpoint
    try:
        model = models[hyper_parameters[
            'name']].load_from_checkpoint(checkpoint_file, **kwargs)
    except RuntimeError:
        # If the model was saved on a GPU and is being loaded on a CPU
        # we need to specify map_location=torch.device('cpu')
        model = models[hyper_parameters[
            'name']].load_from_checkpoint(
                checkpoint_file, map_location=torch.device('cpu'))
    # Put the model in eval mode to fix dropout and other stuff
    model.eval()

    return model
