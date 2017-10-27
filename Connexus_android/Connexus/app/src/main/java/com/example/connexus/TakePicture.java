package com.example.connexus;

import android.app.Activity;
import android.content.ContentUris;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.ByteArrayOutputStream;
import java.util.List;

/**
 * Created by tiffanytillett on 10/21/17.
 */

public class TakePicture extends AppCompatActivity implements GoogleApiClient.OnConnectionFailedListener{

    private ImageButton btn_take;
    private ImageButton btn_use;
    private Button btn_streams;

    public static final String BASE_ENDPOINT = "https://vibrant-mind-177623.appspot.com/";
    private static final String ENDPOINT = BASE_ENDPOINT + "ViewSingleStream/api";
    //private static final String ENDPOINT = "http://10.0.2.2:8080/ViewSingleStream/api";
    //private static final String ENDPOINT = "https://vibrant-mind-177623.appspot.com/ViewSingleStream/api";
    private static final String TAG = TakePicture.class.getSimpleName();
    private RequestQueue requestQueue;
    private List<ImagePost> posts;
    String name;
    int page;
    private Gson gson;
    private ImageView image;

    byte[] photo;
    public static String URL = "Paste your URL here";
    public static final int REQUEST_IMAGE_CAPTURE = 1;

    Activity activity;
    Context context;
    GoogleApiClient mGoogleApiClient;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.take_picture);

        image = (ImageView) findViewById(R.id.picture_preview);
        btn_take = (ImageButton) findViewById(R.id.btn_picture);
        btn_use = (ImageButton) findViewById(R.id.btn_usepic);
        btn_streams = (Button) findViewById(R.id.btn_take_streams);

        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.setDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
        gson = gsonBuilder.create();

        requestQueue = Volley.newRequestQueue(this);
        activity = this;
        context = this;

        Bundle extras = this.getIntent().getExtras();
        if (extras != null) {
            name = extras.getString("stream_name");
        }
        // need to add code here to put the preview in the image view

        btn_take.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                takePicture();
            }
        });

        btn_use.setEnabled(false);
        btn_use.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //need to go back to upload page
                //findViewById(R.id.btn_upload).setEnabled(true);
                Intent intent = new Intent(getApplicationContext(), UploadImages.class);
                Bundle b = new Bundle();
                b.putString("stream_name", name);
                b.putByteArray("photo", photo);
                intent.putExtras(b);
                startActivity(intent);
            }
        });
        btn_streams.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), ViewAllStreams.class);
                startActivity(intent);
            }
        });
    }



    private void takePicture() {

        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }

    }


    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        Uri selectedImageUri = null;

        switch (requestCode) {
            case REQUEST_IMAGE_CAPTURE:
                if (resultCode == RESULT_OK) {
                    Bundle extras = data.getExtras();
                    Bitmap bitmap = (Bitmap) extras.get("data");
                    image.setImageBitmap(bitmap);
                    //selectedImageUri = data.getData();
                    //selectedImageUri = imageUri;
                    //picturePath = getPath(getApplicationContext(), selectedImageUri);
                    //Bitmap bitmap = BitmapFactory.decodeFile(picturePath);
                    ByteArrayOutputStream stream = new ByteArrayOutputStream();
                    bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
                    photo = stream.toByteArray();
                    btn_use.setEnabled(true);
                    //btn_upload.setEnabled(true);
                    /*//use imageUri here to access the image
                    selectedImageUri = imageUri;
                    imagepath2 = selectedImageUri.getPath();
                    //launchUploadActivity(true);
                    Bitmap bitmap = BitmapFactory.decodeFile(imagepath2);
                    //iv.setImageBitmap(bitmap);
                    Log.d(TAG, selectedImageUri.toString());
                    Toast.makeText(this, selectedImageUri.toString(), Toast.LENGTH_SHORT).show(); */

                } else if (resultCode == RESULT_CANCELED) {
                    Toast.makeText(this, "Picture was not taken", Toast.LENGTH_SHORT).show();
                } else {
                    Toast.makeText(this, "Picture was not taken", Toast.LENGTH_SHORT).show();
                }
                break;
        }
    }

    public static String getPath(final Context context, final Uri uri)
    {

        //check here to KITKAT or new version
        final boolean isKitKat = Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT;

        // DocumentProvider
        if (isKitKat && DocumentsContract.isDocumentUri(context, uri)) {

            // ExternalStorageProvider
            if (isExternalStorageDocument(uri)) {
                final String docId = DocumentsContract.getDocumentId(uri);
                final String[] split = docId.split(":");
                final String type = split[0];

                if ("primary".equalsIgnoreCase(type)) {
                    return Environment.getExternalStorageDirectory() + "/" + split[1];
                }
            }
            // DownloadsProvider
            else if (isDownloadsDocument(uri)) {

                final String id = DocumentsContract.getDocumentId(uri);
                final Uri contentUri = ContentUris.withAppendedId(
                        Uri.parse("content://<span id=\"IL_AD1\" class=\"IL_AD\">downloads</span>/public_downloads"), Long.valueOf(id));

                return getDataColumn(context, contentUri, null, null);
            }
            // MediaProvider
            else if (isMediaDocument(uri)) {
                final String docId = DocumentsContract.getDocumentId(uri);
                final String[] split = docId.split(":");
                final String type = split[0];

                Uri contentUri = null;
                if ("image".equals(type)) {
                    contentUri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI;
                } else if ("video".equals(type)) {
                    contentUri = MediaStore.Video.Media.EXTERNAL_CONTENT_URI;
                } else if ("audio".equals(type)) {
                    contentUri = MediaStore.Audio.Media.EXTERNAL_CONTENT_URI;
                }

                final String selection = "_id=?";
                final String[] selectionArgs = new String[] {
                        split[1]
                };

                return getDataColumn(context, contentUri, selection, selectionArgs);
            }
        }
        // MediaStore (and general)
        else if ("content".equalsIgnoreCase(uri.getScheme())) {

            // Return the remote address
            if (isGooglePhotosUri(uri))
                return uri.getLastPathSegment();

            return getDataColumn(context, uri, null, null);
        }
        // File
        else if ("file".equalsIgnoreCase(uri.getScheme())) {
            return uri.getPath();
        }

        return null;
    }

    public static String getDataColumn(Context context, Uri uri, String selection,
                                       String[] selectionArgs) {

        Cursor cursor = null;
        final String column = "_data";
        final String[] projection = {
                column
        };

        try {
            cursor = context.getContentResolver().query(uri, projection, selection, selectionArgs,
                    null);
            if (cursor != null && cursor.moveToFirst()) {
                final int index = cursor.getColumnIndexOrThrow(column);
                return cursor.getString(index);
            }
        } finally {
            if (cursor != null)
                cursor.close();
        }
        return null;
    }

    public static boolean isExternalStorageDocument(Uri uri) {
        return "com.android.externalstorage.documents".equals(uri.getAuthority());
    }


    public static boolean isDownloadsDocument(Uri uri) {
        return "com.android.providers.downloads.documents".equals(uri.getAuthority());
    }


    public static boolean isMediaDocument(Uri uri) {
        return "com.android.providers.media.documents".equals(uri.getAuthority());
    }


    public static boolean isGooglePhotosUri(Uri uri) {
        return "com.google.android.apps.photos.content".equals(uri.getAuthority());
    }


    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        Log.d(TAG, "onConnectionFailed:" + connectionResult);
    }


}
