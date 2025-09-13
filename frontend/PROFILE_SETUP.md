# Profile Setup Instructions

## Adding Your Profile Picture

1. **Prepare your image:**
   - Use a square photo (1:1 aspect ratio)
   - Minimum size: 200x200 pixels
   - Recommended size: 400x400 pixels or larger
   - Supported formats: JPG, PNG, WebP

2. **Add the image:**
   - Replace the file `frontend/public/profile-picture.jpg` with your actual photo
   - Keep the filename exactly as `profile-picture.jpg`
   - The image will automatically appear in:
     - Header (small circular avatar)
     - Sidebar (large circular avatar)
     - Chat messages (AI responses)

## Adding Your Resume

1. **Prepare your resume:**
   - Convert to PDF format
   - Keep file size reasonable (< 5MB)

2. **Add the resume:**
   - Replace the file `frontend/public/resume.pdf` with your actual resume
   - Keep the filename exactly as `resume.pdf`
   - The resume button in the sidebar will link to this file

## Updating LinkedIn URL

In `frontend/src/App.tsx`, find this line (around line 272):
```tsx
href="https://linkedin.com/in/abhinav-gupta"
```

Replace `abhinav-gupta` with your actual LinkedIn username.

## After Making Changes

1. Save the files
2. The changes will automatically appear in the application
3. If you don't see the changes, refresh your browser

## Fallback Behavior

If the profile picture or resume files are missing or can't be loaded:
- Profile picture: Shows a user icon instead
- Resume: Link will show a 404 error (you can update the link to point to your online resume)

## File Structure

```
frontend/
├── public/
│   ├── profile-picture.jpg  ← Your photo goes here
│   └── resume.pdf          ← Your resume goes here
└── src/
    └── App.tsx             ← Update LinkedIn URL here
```
