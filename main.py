from initialsation import *

SEED = 42
IMG_SIZE = 256
N_MAX = None  # use to select only subset of the data N_max = 25 means we use 25 samples from each fold
N_EPOCHS = 1000
BATCH_SIZE = 50
PATIENCE = 10  # FOR EARLY STOPPING
USE_MULTIPROCESSING = True
USE_ALL_FOLDS = True


set_seed(SEED)  # set seed for reproducibility
turn_off_warnings()  # turn of warnings

# LOADING DATA
preprocessing = DataPreprocessing(DATA_PATH, n_max=N_MAX, new_size=(IMG_SIZE, IMG_SIZE))
datasets = preprocessing.get_cv_splits()

# DEFINING THE MODELS THAT WE WANT TO TRAIN - name : (model, target, gamma)
models = {
    "Gender": (model_gender_classification(IMG_SIZE), "gender", None),
    "GenderR4": (model_gender_classification(IMG_SIZE, reducer=4), "gender", None),
    "Age": (model_age_classification(IMG_SIZE), "age", None),
    "Multitask": (model_multitask_classification(IMG_SIZE), "multi", 0.5),
    "Transfer": (model_transfer_multitask_classification(IMG_SIZE), "multi", 0.5),
}

# TRAIN MODELS ON ALL FOLDS AND SAVE THE BEST MODEL FROM THE LAST FOLD AND SAVE THE TRAIN HISTORIES
trainer = Trainer(
    models,
    datasets,
    checkpoint_filepath=CHECKPOINT_PATH,
    histories_filepath=HISTORIES_PATH,
    no_epochs=N_EPOCHS,
    batch_size=BATCH_SIZE,
    patience=PATIENCE,
    all_folds=USE_ALL_FOLDS,
    use_multiprocessing=USE_MULTIPROCESSING,
)

for model in models.keys():
    trainer.train_model(model)
