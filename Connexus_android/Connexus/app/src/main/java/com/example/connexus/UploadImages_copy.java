package com.example.connexus;

/**
 * Created by tiffanytillett on 10/21/17.
 */

/*public class UploadImages_copy extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener{

    private TextView title;
    private TextView subtitle;
    private Button btn_camera;
    private Button btn_library;
    private Button btn_upload;

    private static final String ENDPOINT = "http://10.0.2.2:8080/ViewSingleStream/api";
    private String CurEndpoint;
    private static final String TAG = UploadImages_copy.class.getSimpleName();
    private RequestQueue requestQueue;
    private List<ImagePost> posts;
    String name;
    int page;
    private Gson gson;

    private Uri fileUri;
    String picturePath;
    Uri selectedImage;
    String photo;
    String ba1;
    public static String URL = "Paste your URL here";
    public static final int REQUEST_IMAGE_CAPTURE = 1;
    public static final int GET_FROM_GALLERY = 3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.upload_images);

        title = (TextView) findViewById(R.id.title_upload);
        subtitle = (TextView) findViewById(R.id.subtitle_upload);
        btn_camera = (Button) findViewById(R.id.btn_camera);
        btn_upload = (Button) findViewById(R.id.btn_post_upload);
        btn_library = (Button) findViewById(R.id.btn_library);

        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.setDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
        gson = gsonBuilder.create();

        requestQueue = Volley.newRequestQueue(this);

        Bundle extras = this.getIntent().getExtras();
        if (extras != null) {
            name = extras.getString("stream_name");
            page = extras.getInt("page");
            subtitle.setText("Stream: " + name);
        }

        PackageManager pm = getApplicationContext().getPackageManager();
        if (pm.hasSystemFeature(PackageManager.FEATURE_CAMERA)) {
            btn_camera.setClickable(true);
        }

        View view;
        btn_camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                takePicture();
            }
        });

        btn_library.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                selectPicture();
            }
        });
        btn_upload.setEnabled(false);
        btn_upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                upload();
            }
        });
    }


    private void selectPicture() {
        startActivityForResult(new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.INTERNAL_CONTENT_URI), GET_FROM_GALLERY);

    }

    private void takePicture() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            Bundle extras = data.getExtras();
            Bitmap bitmap = (Bitmap) extras.get("data");
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
            byte[] byteArray = stream.toByteArray();
            photo = byteArray.toString();
            btn_upload.setEnabled(true);
            //mImageView.setImageBitmap(imageBitmap);
        }
        if(requestCode==GET_FROM_GALLERY && resultCode == Activity.RESULT_OK) {
            Uri selectedImageUri = data.getData();
            String imagepath = getPath(selectedImageUri);


            launchUploadActivity2(true);
            Bitmap bitmap=BitmapFactory.decodeFile(imagepath);
            iv.setImageBitmap(bitmap);


            Toast.makeText(this, selectedImageUri.toString(), Toast.LENGTH_SHORT).show();

            /*Uri selectedImage = data.getData();

            // Cursor to get image uri to display

            String[] filePathColumn = {MediaStore.Images.Media.DATA};
            Cursor cursor = getContentResolver().query(selectedImage,
                    filePathColumn, null, null, null);
            cursor.moveToFirst();

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            picturePath = cursor.getString(columnIndex);
            cursor.close();

            Bitmap bitmap = (Bitmap) data.getExtras().get("data"); */

            /*Uri selectedImage = data.getData();

            String[] filePathColumn = {MediaStore.Images.Media.DATA};
            Cursor cursor = getContentResolver().query(selectedImage,
                    filePathColumn, null, null, null);
            cursor.moveToFirst();

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            picturePath = cursor.getString(columnIndex);
            cursor.close();
            //realPath = RealPathUtil.getRealPathFromURI_API19(this, data.getData());

            /*Bitmap image = (Bitmap) data.getExtras().get("data");
            ByteArrayOutputStream stream = new ByteArrayOutputStream();
            image.compress(Bitmap.CompressFormat.JPEG, 100, stream);
            byte[] byteArray = stream.toByteArray();
            photo = byteArray.toString(); */

            /*File file = new File(picturePath);

            Uri uriFromPath = Uri.fromFile(file);

            // you have two ways to display selected image

            // ( 1 ) imageView.setImageURI(uriFromPath);

            // ( 2 ) imageView.setImageBitmap(bitmap);
            Bitmap bitmap = null;
            try {
                bitmap = BitmapFactory.decodeStream(getContentResolver().openInputStream(uriFromPath));
                ByteArrayOutputStream stream = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
                byte[] byteArray = stream.toByteArray();
                photo = byteArray.toString();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            //imageView.setImageBitmap(bitmap);
            //photo = file.toString();
            btn_upload.setEnabled(true); */

            /*try {
                Bitmap bitmap = MediaStore.Images.Media.getBitmap(this.getContentResolver(), selectedImage);
                ByteArrayOutputStream stream = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
                byte[] byteArray = stream.toByteArray();
                //photo = byteArray.toString();
                btn_upload.setEnabled(true);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } */
  /*      }
    }


    private void upload() {
        StringRequest request = new StringRequest(Request.Method.POST, ENDPOINT, onPostsLoaded_post, onPostsError)
        {
            @Override
            protected Map<String, String> getParams(){
                Map<String, String> params = new HashMap<String, String>();
                params.put("stream_name", name);
                params.put("page", Integer.toString(page));
                params.put("file", photo);
                params.put("name", "dummy");
                return params;
            }
        };
        requestQueue.add(request); */
        /*picture_name
                page
                stream_name */


  /*  }

    private final Response.Listener<String> onPostsLoaded_post = new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
            posts = Arrays.asList(gson.fromJson(response, ImagePost[].class));
            int size = posts.size();
            Log.i("PostActivity", size + " posts loaded.");
            int page = posts.get(0).page;
            Intent intent = new Intent(getApplicationContext(), ViewStream.class);
            Bundle b = new Bundle();
            b.putString("stream_name", name);
            b.putInt("page", page);
            intent.putExtras(b);
            startActivity(intent);

        }
    };

    private final Response.ErrorListener onPostsError = new Response.ErrorListener() {
        @Override
        public void onErrorResponse(VolleyError error) {
            Log.e("PostActivity", error.toString());
        }
    };
 */

     /*private void takePicture() {
        // Check Camera
        if (getApplicationContext().getPackageManager().hasSystemFeature(
                PackageManager.FEATURE_CAMERA)) {
            // Open default camera
            Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
            intent.putExtra(MediaStore.EXTRA_OUTPUT, fileUri);

            // start the image capture Intent
            startActivityForResult(intent, 100);

        } else {
            Toast.makeText(getApplication(), "Camera not supported", Toast.LENGTH_LONG).show();
        }
    } */

    /*private void upload(Bitmap photo) {
        // Image location URL
        Log.e("path", "----------------" + picturePath);

        // Image
        Bitmap bm = BitmapFactory.decodeFile(picturePath);
        ByteArrayOutputStream bao = new ByteArrayOutputStream();
        bm.compress(Bitmap.CompressFormat.JPEG, 90, bao);
        byte[] ba = bao.toByteArray();
        //ba1 = Base64.encodeBytes(ba);

        Log.e("base64", "-----" + ba1);

        // Upload image to server
        new uploadToServer().execute();

    }



    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 100 && resultCode == RESULT_OK) {

            selectedImage = data.getData();
            photo = (Bitmap) data.getExtras().get("data");

            // Cursor to get image uri to display

            String[] filePathColumn = {MediaStore.Images.Media.DATA};
            Cursor cursor = getContentResolver().query(selectedImage,
                    filePathColumn, null, null, null);
            cursor.moveToFirst();

            int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
            picturePath = cursor.getString(columnIndex);
            cursor.close();

            Bitmap photo = (Bitmap) data.getExtras().get("data");
            upload(photo);
            //ImageView imageView = (ImageView) findViewById(R.id.Imageprev);
            //imageView.setImageBitmap(photo);
        }
    }

    public class uploadToServer extends AsyncTask<Void, Void, String> {

        //private ProgressDialog pd = new ProgressDialog(MainActivity.this);
        protected void onPreExecute() {
            super.onPreExecute();
            *//*pd.setMessage("Wait image uploading!");
            pd.show(); */
       /* }

        @Override
        protected String doInBackground(Void... params) {

          */  /*ArrayList<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();
            nameValuePairs.add(new BasicNameValuePair("base64", ba1));
            nameValuePairs.add(new BasicNameValuePair("ImageName", System.currentTimeMillis() + ".jpg"));
            try {
                HttpClient httpclient = new DefaultHttpClient();
                HttpPost httppost = new HttpPost(URL);
                httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
                HttpResponse response = httpclient.execute(httppost);
                String st = EntityUtils.toString(response.getEntity());
                Log.v("log_tag", "In the try Loop" + st);

            } catch (Exception e) {
                Log.v("log_tag", "Error in http connection " + e.toString());
            } */
        /*    return "Success";

        }

        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            //pd.hide();
            //pd.dismiss();
        }
    }
 */
   /* @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        Log.d(TAG, "onConnectionFailed:" + connectionResult);
    }


} */
