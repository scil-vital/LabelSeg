from os.path import isfile

import lightning.pytorch as pl

from torch.utils.data import DataLoader, random_split

from LabelSeg.dataset.fodf_dataset import FODFDataset
from LabelSeg.dataset.fodf_file_dataset import FODFFileDataset


class FODFDataModule(pl.LightningDataModule):
    """
    """

    def __init__(
        self,
        train_file: str,
        val_file: str = None,
        test_file: str = None,
        subfolder: str = '',
        batch_size: int = 1,
        num_workers: int = 10,
    ):
        """

        Parameters:
        -----------
        train_file: str
            Path to the hdf5 file containing the training set
        val_file: str
            Path to the hdf5 file containing the validation set
        test_file: str
            Path to the hdf5 file containing the test set
        batch_size: int, optional
            Size of the batches to use for the dataloaders
        num_workers: int, optional
            Number of workers to use for the dataloaders
        """

        super().__init__()
        self.train_file = train_file
        self.val_file = val_file
        self.test_file = test_file
        self.subfolder = subfolder
        self.batch_size = batch_size
        self.num_workers = num_workers

        self.save_hyperparameters()

        self.data_loader_kwargs = {
            'batch_size': self.batch_size,
            'num_workers': self.num_workers,
            'prefetch_factor': None,
            'persistent_workers': False,
            'pin_memory': False
        }

        # self.transform = transforms.Compose([
        #     transforms.ToTensor(),
        #     transforms.NormalizeIntensity()])
        self.transform = None

    def prepare_data(self):
        pass

    def setup(self, stage: str):

        if self.val_file is None and self.test_file is None:

            if isfile(self.train_file[0]):
                whole_data = FODFDataset(
                    self.train_file[0], self.transform)
            else:
                whole_data = FODFFileDataset(
                    self.train_file[0], subfolder=self.subfolder,
                    transforms=self.transform)
            self.train, self.val, self.test = \
                random_split(whole_data, [0.70, 0.20, 0.10])
        else:
            # Assign train/val datasets for use in dataloaders
            self.train = FODFDataset(
                self.train_file, self.transform)

            self.val = FODFDataset(
                self.val_file, self.transform)

            # Assign test dataset for use in dataloader(s)
            self.test = FODFDataset(
                self.test_file, self.transform)

    def train_dataloader(self):
        """ Create the dataloader for the training set
        """
        train_kwargs = self.data_loader_kwargs.copy()
        train_kwargs.update({'shuffle': True})
        return DataLoader(
            self.train,
            **train_kwargs)

    def val_dataloader(self):
        """ Create the dataloader for the validation set
        """
        return DataLoader(
            self.val,
            **self.data_loader_kwargs)

    def test_dataloader(self):
        """ Create the dataloader for the test set
        """
        return DataLoader(
            self.test,
            **self.data_loader_kwargs)

    def predict_dataloader(self):
        pass
