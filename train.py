from ultralytics import YOLO
import torch
import yaml
from pathlib import Path
import wandb  # Import wandb library
def create_custom_yaml():
    “”"Create custom training configuration file”“”
    config = {
        ‘path’: ‘../military_object_dataset’,  # Dataset root directory
        ‘train’: ‘../military_object_dataset/train’,  # Training set path
        ‘val’: ‘../military_object_dataset/val’,      # Validation set path
        ‘test’: ‘../military_object_dataset/test’,    # Test set path
        ‘names’: {
            0: ‘camouflage_soldier’,
            1: ‘weapon’,
            2: ‘military_tank’,
            3: ‘military_truck’,
            4: ‘military_vehicle’,
            5: ‘civilian’,
            6: ‘soldier’,
            7: ‘civilian_vehicle’,
            8: ‘military_artillery’,
            9: ‘trench’,
            10: ‘military_aircraft’,
            11: ‘military_warship’
        }
    }
    # Save configuration file
    with open(‘custom_dataset.yaml’, ‘w’) as f:
        yaml.dump(config, f)
    return ‘custom_dataset.yaml’
def main():
    # Initialize wandb
    wandb.init(project=“military-object-detection”, name=“yolov8s-training”)
    # Create custom configuration file
    data_yaml = create_custom_yaml()
    # Load pre-trained model
    model = YOLO(“yolov8s.pt”)  # Use small version instead of nano version
    # Training parameter configuration
    results = model.train(
        data=data_yaml,
        epochs=50,
        imgsz=640,
        batch=32,
        device=‘0’ if torch.cuda.is_available() else ‘cpu’,
        # Optimizer configuration
        lr0=0.01,
        lrf=0.1,
        momentum=0.937,
        weight_decay=0.0005,
        # Data augmentation configuration
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=15,
        translate=0.2,
        scale=0.5,
        shear=2,
        perspective=0.0,
        flipud=0.5,
        fliplr=0.5,
        mosaic=1.0,
        mixup=0.5,
        # Training strategy
        warmup_epochs=3,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        # Early stopping configuration
        patience=10,
        # Save configuration
        save=True,
        save_period=5,
        project=‘runs/train’,
        name=‘yolov8s-training’,
        exist_ok=True,
        # Validation configuration
        val=True,
        plots=True,
    )
    # Complete wandb run
    wandb.finish()
if __name__ == “__main__“:
    main()