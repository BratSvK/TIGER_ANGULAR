import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { faCloudUpload } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'ImageUploader',
  templateUrl: './image-uploader.component.html',
  styleUrl: './image-uploader.component.scss'
})
export class ImageUploaderComponent {
  @Output() onUploadedTissue = new EventEmitter<File>();
  @Input() isEnabled: boolean;
  @ViewChild('fileInput') fileInput: ElementRef;
  cloudIcon = faCloudUpload;

  openFileInput() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
      fileInput.click();
    }
  }

  onFileSelected(event: any) {
    const selectedFile: File = event.target.files[0];
    this.onUploadedTissue.emit(selectedFile);
    this.fileInput.nativeElement.value = '';
  }
}
