from functools import partial

try:
    from sklearn.metrics import average_precision_score
except ImportError:
    raise RuntimeError("This contrib module requires sklearn to be installed")

from ignite.metrics import EpochMetric


def average_precision_compute_fn(y_preds, y_targets, activation=None):
    y_true = y_targets.numpy()
    if activation is not None:
        y_preds = activation(y_preds)
    y_pred = y_preds.numpy()
    return average_precision_score(y_true, y_pred)


class AveragePrecision(EpochMetric):
    """Computes Average Precision accumulating predictions and the ground-truth during an epoch
    and applying `sklearn.metrics.average_precision_score <http://scikit-learn.org/stable/modules/generated/
    sklearn.metrics.average_precision_score.html#sklearn.metrics.average_precision_score>`_

    Args:
        activation (Callable, optional): optional function to apply on prediction tensors,
            e.g. `activation=torch.sigmoid` to transform logits.
    """
    def __init__(self, activation=None):
        super(AveragePrecision, self).__init__(partial(average_precision_compute_fn, activation=activation))
