package com.example.connexus;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.GridView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ViewStream extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener{


    private MyApplication myApplication;
    private GoogleApiClient mGoogleApiClient;
    private Context mContext;
    private static final String TAG = MainActivity.class.getSimpleName();
    private ArrayList<Bitmap> bitmapList;
    private Gson gson;

    private TextView title;
    private GridView imageGrid;
    private Button btn_view_streams;
    private Button btn_upload;
    //private static final String ENDPOINT = "https://kylewbanks.com/rest/posts.json";
    private static final String ENDPOINT = "http://10.0.2.2:8080/ViewSingleStream/api";
    //private static final String ENDPOINT = "http://10.0.2.2:8080/ViewAllStream/api";
    private String CurEndpoint;

    private RequestQueue requestQueue;
    private List<ImagePost> posts;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_stream);

        myApplication = (MyApplication)getApplicationContext();
        title = (TextView) findViewById(R.id.title2);
        imageGrid = (GridView) findViewById(R.id.gridview2);
        btn_view_streams = (Button) findViewById(R.id.btn_view_streams);
        btn_upload = (Button) findViewById(R.id.btn_upload);
        this.bitmapList = new ArrayList<Bitmap>();
        updateUI(true);

        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.setDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
        gson = gsonBuilder.create();

        //http://127.0.0.1:8080/ViewSingleStream/api?stream_name=me
        Bundle extras = this.getIntent().getExtras();
        if (extras != null) {
            String name = extras.getString("stream_name");
            CurEndpoint = ENDPOINT + "?stream_name=" + name;
            requestQueue = Volley.newRequestQueue(this);
            fetchPosts();
        }


    }

    private void fetchPosts() {
        StringRequest request = new StringRequest(Request.Method.GET, CurEndpoint, onPostsLoaded, onPostsError);
        requestQueue.add(request);
    }

    private final Response.Listener<String> onPostsLoaded = new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
            posts = Arrays.asList(gson.fromJson(response, ImagePost[].class));

            ArrayList<String> images = new ArrayList<String>();
            ArrayList<String> names = new ArrayList<String>();

            Log.i("PostActivity", posts.size() + " posts loaded.");
            for (ImagePost post : posts) {
                //ArrayList<String> pics = post.pics;
                //for (String image : pics) {
                String image = post.pic;
                    String fixedStr = image.replaceAll("127.0.0.1", "10.0.2.2");
                    images.add(fixedStr);
                    //names.add(post.name);
                    names.add("");
               // }

            }

           for (int i = images.size(); i < 16; i++)
            {
                images.add("");
                names.add("");
            }

            String[] imageArr = new String[images.size()];
            imageArr = images.toArray(imageArr);
            String[] nameArr = new String[names.size()];
            nameArr = names.toArray(nameArr);


            GridView gridview = (GridView) findViewById(R.id.gridview2);
            gridview.setAdapter(new ImageAdapter(ViewStream.this, imageArr, nameArr));

            btn_view_streams.setOnClickListener(new View.OnClickListener() {
                public void onClick(View v) {
                    Intent intent = new Intent(getApplicationContext(), ViewAllStreams.class);
                    startActivity(intent);
                }
            });

        }
    };

    private final Response.ErrorListener onPostsError = new Response.ErrorListener() {
        @Override
        public void onErrorResponse(VolleyError error) {
            Log.e("PostActivity", error.toString());
        }
    };

    private Bitmap urlImageToBitmap(String imageUrl) throws Exception {
        Bitmap result = null;
        URL url = new URL(imageUrl);
        if(url != null) {
            result = BitmapFactory.decodeStream(url.openConnection().getInputStream());
        }
        return result;
    }


    public void uploadImage(View view) {
        Intent intent = new Intent(this, UploadImages.class);
        startActivity(intent);
    }

    public void uploadImage() {
        Intent intent = new Intent(this, UploadImages.class);
        startActivity(intent);
    }



    //****************************************END OF NETWORKING CODE**************************************//*

    //*********************************************LOGIN CODE*********************************************//*

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        Log.d(TAG, "onConnectionFailed:" + connectionResult);
    }

    private void updateUI(boolean isSignedIn) {
        getSupportActionBar().setDisplayHomeAsUpEnabled(false);
        getSupportActionBar().setHomeButtonEnabled(false);
        if (isSignedIn) {
            title.setVisibility(View.VISIBLE);
            imageGrid.setVisibility(View.VISIBLE);
            //btn_sign_out.setVisibility(View.VISIBLE);
            //btn_sign_in.setVisibility(View.GONE);
            btn_upload.setVisibility(View.VISIBLE);
            btn_view_streams.setVisibility(View.VISIBLE);
        } else {
            title.setVisibility(View.VISIBLE);
            imageGrid.setVisibility(View.VISIBLE);
            //btn_sign_out.setVisibility(View.GONE);
            //btn_sign_in.setVisibility(View.VISIBLE);
            btn_upload.setVisibility(View.VISIBLE);
            btn_view_streams.setVisibility(View.VISIBLE);
        }
    }
}


