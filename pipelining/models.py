from django.db import models

# Create your models here.
class Pipeline(models.Model):
    # Unique identifier for the pipeline
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Tracks the creation and modification timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata about the pipeline
    status_choices = [
        ('Pending', 'Pending'),
        ('Running', 'Running'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]
    status = models.CharField(max_length=50, choices=status_choices, default='Pending')
    version = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Step(models.Model):
    # Each step is associated with a pipeline
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name="steps")
    
    # The step name and its execution order
    name = models.CharField(max_length=255)
    order = models.IntegerField()
    
    # Information about the step
    step_type = models.CharField(max_length=255)  # Could be 'Data Processing', 'Training', 'Evaluation', etc.
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Running', 'Running'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ], default='Pending')

    # Additional info
    execution_time = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"Step {self.order}: {self.name}"

class ModelArtifact(models.Model):
    # Reference to the pipeline and step
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="artifacts")
    
    # Model file location and metadata
    model_file = models.FileField(upload_to='models/')
    accuracy = models.FloatField(blank=True, null=True)
    loss = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return f"Model artifact for step: {self.step.name}"
