import time

from package.loader import load_pickle
from package.utils import save_pickle


class CheckPoint:
    """
    The Checkpoint class manages the saving and loading of a model during training. It allows training to be suspended
    and resumed at a later time (e.g. when running on a cluster using sequential jobs).

    To make a checkpoint, initialize a Checkpoint object with the following args; then call that object's save() method
    to write parameters to disk.

    Args:
        model (torch.nn.Module): seq2seq model being trained
        optimizer (torch.nn): stores the state of the optimizer
        epoch (int): current epoch (an epoch is a loop through the full training data)
        time_step (int): number of examples seen within the current epoch
        batch_size (int): mini batch size

    """
    CHECKPOINT_DIR = './data/checkpoints/'

    def __init__(self, model=None, optimizer=None, epoch=None, train_dataset_list=None, valid_dataset=None, time_step=None,
                 total_time_step=None, batch_size=None, hparams=None, train_queue=None, criterion=None):
        self.snapshot = dict()
        self.snapshot['model'] = model
        self.snapshot['optimizer'] = optimizer
        self.snapshot['train_dataset_list'] = train_dataset_list
        self.snapshot['valid_dataset'] = valid_dataset
        self.snapshot['epoch'] = epoch
        self.snapshot['total_time_step'] = total_time_step
        self.snapshot['time_step'] = time_step
        self.snapshot['batch_size'] = batch_size
        self.snapshot['hparams'] = hparams
        self.snapshot['train_queue'] = train_queue
        self.snapshot['criterion'] = criterion

    def save(self, model=None, optimizer=None, epoch=None, train_dataset_list=None, valid_dataset=None, time_step=None,
             total_time_step=None, batch_size=None, loss=None, cer=None, hparams=None, train_queue=None,
             total_loss=None, total_num=None, total_dist=None, total_length=None, total_sent_num=None, worker_num=None):
        if model is not None:
            self.snapshot['model'] = model
        if optimizer is not None:
            self.snapshot['optimizer'] = optimizer
        if train_dataset_list is not None:
            self.snapshot['train_dataset_list'] = train_dataset_list
        if valid_dataset is not None:
            self.snapshot['valid_dataset'] = valid_dataset
        if epoch is not None:
            self.snapshot['epoch'] = epoch
        if total_time_step is not None:
            self.snapshot['total_time_step'] = total_time_step
        if time_step is not None:
            self.snapshot['time_step'] = time_step
        if batch_size is not None:
            self.snapshot['batch_size'] = batch_size
        if loss is not None:
            self.snapshot['loss'] = loss
        if cer is not None:
            self.snapshot['cer'] = cer
        if hparams is not None:
            self.snapshot['hparams'] = hparams
        if train_queue is not None:
            self.snapshot['train_queue'] = train_queue
        if total_loss is not None:
            self.snapshot['total_loss'] = total_loss
        if total_num is not None:
            self.snapshot['total_num'] = total_num
        if total_dist is not None:
            self.snapshot['total_dist'] = total_dist
        if total_length is not None:
            self.snapshot['total_length'] = total_length
        if total_sent_num is not None:
            self.snapshot['total_sent_num'] = total_sent_num
        if worker_num is not None:
            self.snapshot['worker_num'] = worker_num

        date_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        path = self.CHECKPOINT_DIR + date_time + '.bin'
        save_pickle(self.snapshot, path, message="snapshot : %s save" % path)

    def load(self, path):
        self.snapshot = load_pickle(path, "load snapshot...")
        return self.snapshot