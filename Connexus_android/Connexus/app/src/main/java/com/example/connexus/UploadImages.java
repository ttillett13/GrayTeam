package com.example.connexus;

import android.Manifest;
import android.app.Activity;
import android.content.ContentUris;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.location.Location;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.LocationServices;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.UnsupportedEncodingException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by tiffanytillett on 10/21/17.
 */

public class UploadImages  extends AppCompatActivity
        implements GoogleApiClient.ConnectionCallbacks,
        GoogleApiClient.OnConnectionFailedListener,
        ActivityCompat.OnRequestPermissionsResultCallback  {
 /*   public class UploadImages extends AppCompatActivity implements
            GoogleApiClient.OnConnectionFailedListener{ */

    private TextView subtitle;
    private TextView comments;
    private Button btn_camera;
    private Button btn_library;
    private Button btn_upload;

    public static final String BASE_ENDPOINT = "http://vibrant-mind-177623.appspot.com/";
    //public static final String BASE_ENDPOINT = "http://10.0.2.2:8080/";
    private static final String ENDPOINT = BASE_ENDPOINT + "ViewSingleStream/api";
    private String CurEndpoint;
    private static final String TAG = UploadImages.class.getSimpleName();
    private RequestQueue requestQueue;
    private List<ImagePost> posts;
    String name;
    int page;
    private Gson gson;
    private ImageView image;

    private Uri fileUri;
    String picturePath;
    Uri selectedImage;
    //String photo;
    byte[] photo;
    String ba1;
    public static String URL = "Paste your URL here";
    public static final int REQUEST_IMAGE_CAPTURE = 1;
    public static final int GET_FROM_GALLERY = 3;
    public static final int GET_LOCATION = 2;

    String filePath;
    String imagePath;
    String imagepath2;
    Uri imageUri;
    int count;
    public static String dir;

    Activity activity;
    Context context;
    GoogleApiClient mGoogleApiClient;
    private Location mLastLocation;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.upload_images);

        subtitle = (TextView) findViewById(R.id.subtitle_upload);
        comments = (TextView) findViewById(R.id.te_comments_tags);
        comments.setText("");
        btn_camera = (Button) findViewById(R.id.btn_camera);
        btn_upload = (Button) findViewById(R.id.btn_post_upload);
        btn_library = (Button) findViewById(R.id.btn_library);

        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.setDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
        gson = gsonBuilder.create();

        requestQueue = Volley.newRequestQueue(this);
        activity = this;
        context = this;
        count = 0;
        dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES) + "/picFolder/";
        File newdir = new File(dir);
        newdir.mkdirs();

        Intent intent = this.getIntent();
        Bundle extras = intent.getExtras();
        if (extras != null) {
            name = extras.getString("stream_name");
            if (intent.hasExtra("page")) {
                page = extras.getInt("page");
            }
            if (intent.hasExtra("photo")) {
                photo = extras.getByteArray("photo");
                btn_upload.setEnabled(true);
            } else {
                btn_upload.setEnabled(false);
            }
            subtitle.setText("Stream: " + name);
        }

        PackageManager pm = getApplicationContext().getPackageManager();
        if (pm.hasSystemFeature(PackageManager.FEATURE_CAMERA)) {
            btn_camera.setClickable(true);
        }

        btn_camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                try {
                    if (ActivityCompat.checkSelfPermission(context, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                        ActivityCompat.requestPermissions(activity, new String[]{Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE}, REQUEST_IMAGE_CAPTURE);
                    } else {
                        takePicture();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });


        btn_library.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //selectPicture();
                try {
                    if (ActivityCompat.checkSelfPermission(context, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                        ActivityCompat.requestPermissions(activity, new String[]{Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE}, GET_FROM_GALLERY);
                    } else {
                        selectPicture();
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });


        btn_upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                upload();
            }
        });
        initLocation();
        processCurrentLocation();
    }

    private void upload() {
        VolleyMultipartRequest multipartRequest = new VolleyMultipartRequest(Request.Method.POST, ENDPOINT, new Response.Listener<NetworkResponse>() {
            @Override
            public void onResponse(NetworkResponse response) {
                String resultResponse = new String(response.data);
                String json = "";
                try {
                    json = new String(response.data,
                        HttpHeaderParser.parseCharset(response.headers));
                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                }

                posts = Arrays.asList(gson.fromJson(json, ImagePost[].class));
                int size = posts.size();
                Log.i("PostActivity", size + " posts loaded.");
                int page = posts.get(0).page;
                finish();

                Intent intent = new Intent(getApplicationContext(), ViewStream.class);
                Bundle b = new Bundle();
                b.putString("stream_name", name);
                b.putInt("page", page);
                intent.putExtras(b);
                startActivity(intent);

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
            }
        }) {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<>();
                params.put("stream_name", name);
                params.put("page", Integer.toString(page));
                params.put("name", "connexus" + Integer.toBinaryString(count));
                String text = comments.getText().toString();
                params.put("comments", text);
                if (mLastLocation != null) {
                    params.put("latitude", Double.toString(mLastLocation.getLatitude()));
                    params.put("longitude", Double.toString(mLastLocation.getLongitude()));
                }
                count++;
                return params;
            }

            @Override
            protected Map<String, DataPart> getByteData() {
                Map<String, DataPart> params = new HashMap<>();
                // file name could found file base or direct access from real path
                // for now just get bitmap data from ImageView
                params.put("file", new DataPart(picturePath, photo, "image/jpeg"));
                return params;
            }
        };
        requestQueue.add(multipartRequest);
    }

    private void initLocation() {
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .addConnectionCallbacks(this)
                .addOnConnectionFailedListener(this)
                .addApi(LocationServices.API).build();
        mGoogleApiClient.connect();
    }
    private void processCurrentLocation() {
        try {
            if ((ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED)
                    || (ActivityCompat.checkSelfPermission(context, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED)) {
                ActivityCompat.requestPermissions(activity, new String[]{Manifest.permission.ACCESS_FINE_LOCATION,
                        Manifest.permission.ACCESS_COARSE_LOCATION}, GET_LOCATION);
            } else {
                mLastLocation = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);
                /*if (mLastLocation != null) {
                    Toast.makeText(this, mLastLocation.getLatitude() + " : " + mLastLocation.getLongitude(), Toast.LENGTH_LONG).show();
                }  */
           }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public void onPostsLoaded(NetworkResponse response) {
        String resultResponse = new String(response.data);
        String json = "";
        try {
            json = new String(response.data,
                    HttpHeaderParser.parseCharset(response.headers));
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        posts = Arrays.asList(gson.fromJson(json, ImagePost[].class));
        int size = posts.size();
        Log.i("PostActivity", size + " posts loaded.");
        int page = posts.get(0).page;
        finish();
        Intent intent = new Intent(getApplicationContext(), ViewStream.class);
        Bundle b = new Bundle();
        b.putString("stream_name", name);
        b.putInt("page", page);
        intent.putExtras(b);
        startActivity(intent);
    }


    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        //processCurrentLocation();
    }

    private void selectPicture() {
        startActivityForResult(new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.INTERNAL_CONTENT_URI), GET_FROM_GALLERY);

    }

    private void takePicture() {
        Intent intent = new Intent(getApplicationContext(), TakePicture.class);
        Bundle b = new Bundle();
        b.putString("stream_name", name);
        intent.putExtras(b);
        startActivity(intent);
        finish();
    }


    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        Uri selectedImageUri = null;

        switch (requestCode) {
            case GET_FROM_GALLERY:
                if (resultCode == Activity.RESULT_OK) {
                    selectedImageUri = data.getData();
                    picturePath = getPath(getApplicationContext(), selectedImageUri);
                    Bitmap bitmap = BitmapFactory.decodeFile(picturePath);
                    ByteArrayOutputStream stream = new ByteArrayOutputStream();
                    bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
                    photo = stream.toByteArray();
                    btn_upload.setEnabled(true);
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


    @Override
    public void onConnected(Bundle arg0) {
        processCurrentLocation();
    }

    @Override
    public void onConnectionSuspended(int arg0) {
        mGoogleApiClient.connect();
    }



}
