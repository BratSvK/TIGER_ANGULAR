import { Component } from '@angular/core';
import { faCloudUpload } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'ImageUploader',
  templateUrl: './image-uploader.component.html',
  styleUrl: './image-uploader.component.scss'
})
export class ImageUploaderComponent {
  cloudIcon = faCloudUpload;

  openFileInput() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
      fileInput.click();
    }
  }

  onFileSelected(event: any) {
    // Do something with the selected file, e.g., upload it
    const selectedFile = event.target.files[0];
    console.log('Selected File:', selectedFile);
  }
}
