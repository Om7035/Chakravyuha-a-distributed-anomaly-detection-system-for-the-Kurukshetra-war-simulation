# ml/train_model.py
import pytorch_lightning as pl
from pytorch_forecasting import TemporalFusionTransformer, TimeSeriesDataSet
from pytorch_forecasting.data import GroupNormalizer
from pytorch_forecasting.metrics import QuantileLoss
import pandas as pd
import torch
import os

def train_model():
    print("🚀 Starting Local Training...")
    
    # 1. Load Data (Mocking the Kafka stream for training)
    # In a real scenario, you'd read from the Feature Store's offline parquet file
    # Here we generate synthetic data matching the simulator's logic
    print("Generating synthetic training data...")
    data = pd.DataFrame({
        "time_idx": range(10000),
        "soldier_id": ["0"] * 10000, # Training on single soldier history for simplicity
        "heart_rate": [70 + (i%10) for i in range(10000)],
        "stamina": [100 - (i%20) for i in range(10000)],
    })
    
    # 2. Define Dataset
    max_prediction_length = 10
    max_encoder_length = 30
    training_cutoff = data["time_idx"].max() - max_prediction_length

    training = TimeSeriesDataSet(
        data[lambda x: x.time_idx <= training_cutoff],
        time_idx="time_idx",
        target="heart_rate",
        group_ids=["soldier_id"],
        min_encoder_length=max_encoder_length // 2,
        max_encoder_length=max_encoder_length,
        min_prediction_length=1,
        max_prediction_length=max_prediction_length,
        static_reals=[],
        time_varying_known_reals=["time_idx"],
        time_varying_unknown_reals=["heart_rate", "stamina"],
        target_normalizer=GroupNormalizer(
            groups=["soldier_id"], transformation="softplus"
        ),
        add_relative_time_idx=True,
        add_target_scales=True,
        add_encoder_length=True,
    )

    validation = TimeSeriesDataSet.from_dataset(training, data, predict=True, stop_randomization=True)
    
    batch_size = 64
    train_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=0)
    val_dataloader = validation.to_dataloader(train=False, batch_size=batch_size * 10, num_workers=0)

    # 3. Create Model
    tft = TemporalFusionTransformer.from_dataset(
        training,
        learning_rate=0.03,
        hidden_size=16,
        attention_head_size=1,
        dropout=0.1,
        hidden_continuous_size=8,
        output_size=7,  # 7 quantiles by default
        loss=QuantileLoss(),
        log_interval=10,
        reduce_on_plateau_patience=4,
    )

    # 4. Train
    print("Training model...")
    trainer = pl.Trainer(
        max_epochs=1,
        accelerator="cpu", 
        gradient_clip_val=0.1,
        limit_train_batches=30, # Limit for speed in demo
    )
    
    trainer.fit(
        tft,
        train_dataloaders=train_dataloader,
        val_dataloaders=val_dataloader,
    )
    
    # 5. Save Model
    best_model_path = trainer.checkpoint_callback.best_model_path
    print(f"✅ Best model saved at: {best_model_path}")
    
    # Save as TorchScript for deployment
    best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)
    
    # Note: Exporting TFT to TorchScript can be complex due to dict outputs.
    # For this tutorial, we will just save the checkpoint path to a file for the app to read.
    with open("serving/model_path.txt", "w") as f:
        f.write(best_model_path)
    print("✅ Model path saved for serving.")

if __name__ == "__main__":
    train_model()
