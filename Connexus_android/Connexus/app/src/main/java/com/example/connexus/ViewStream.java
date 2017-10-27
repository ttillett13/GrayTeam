package com.example.connexus;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
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

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ViewStream extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener{


    private MyApplication myApplication;
    private GoogleApiClient mGoogleApiClient;
    private Context mContext;
    private static final String TAG = ViewStream.class.getSimpleName();
    private ArrayList<Bitmap> bitmapList;
    private Gson gson;

    private TextView title;
    private TextView subtitle;
    private GridView imageGrid;
    private Button btn_view_streams;
    private Button btn_upload;
    private Button btn_more_images;
    public static final String BASE_ENDPOINT = "https://vibrant-mind-177623.appspot.com/";
    //private static final String ENDPOINT = "https://kylewbanks.com/rest/posts.json";
    private static final String ENDPOINT = BASE_ENDPOINT + "ViewSingleStream/api";
    //private static final String ENDPOINT = "http://10.0.2.2:8080/ViewAllStream/api";
    private String CurEndpoint;

    private RequestQueue requestQueue;
    private List<ImagePost> posts;
    private int page;
    String name;

    private int start;
    private static final int numPerPage = 16;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.view_stream);

        myApplication = (MyApplication)getApplicationContext();
        title = (TextView) findViewById(R.id.title2);
        subtitle = (TextView) findViewById(R.id.subtitle);
        imageGrid = (GridView) findViewById(R.id.gridview2);
        btn_view_streams = (Button) findViewById(R.id.btn_view_streams);
        btn_upload = (Button) findViewById(R.id.btn_upload);
        btn_more_images = (Button) findViewById(R.id.btn_more_images);
        this.bitmapList = new ArrayList<Bitmap>();
        page = 0;
        start = 0;

        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.setDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
        gson = gsonBuilder.create();

        //http://127.0.0.1:8080/ViewSingleStream?stream_name=flags;status=success;page=7
        Bundle extras = this.getIntent().getExtras();
        if (extras != null) {
            name = extras.getString("stream_name");
            page = extras.getInt("page");
            updateUI();
            CurEndpoint = ENDPOINT + "?stream_name=" + name + ";status=success;page=" + page;
            requestQueue = Volley.newRequestQueue(this);
            fetchPosts();
        }


        btn_view_streams.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), ViewAllStreams.class);
                startActivity(intent);
            }
        });
        btn_more_images.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                //updatePage();
                DisplayImages();
            }
        });
        btn_upload.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), UploadImages.class);
                Bundle b = new Bundle();
                b.putString("stream_name", name);
                intent.putExtras(b);
                startActivity(intent);
            }
        });


    }

    private void fetchPosts() {
        StringRequest request = new StringRequest(Request.Method.GET, CurEndpoint, onPostsLoaded, onPostsError);
        requestQueue.add(request);
    }

    private void updatePage() {
        StringRequest request = new StringRequest(Request.Method.POST, ENDPOINT, onPostsLoaded_post, onPostsError)
        {
            @Override
            protected Map<String, String> getParams(){
                Map<String, String> params = new HashMap<String, String>();
                params.put("stream_name", name);
                params.put("status", "success");
                params.put("decrementPage", Integer.toString(page-15));
                return params;
            }
        };
        requestQueue.add(request);
    }



    private final Response.Listener<String> onPostsLoaded = new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
            posts = Arrays.asList(gson.fromJson(response, ImagePost[].class));
            DisplayImages();
        }
    };

    void DisplayImages() {
        ArrayList<String> images = new ArrayList<String>();
        int size = posts.size();
        Log.i("PostActivity", size + " posts loaded.");
        int stop = start + Math.min(numPerPage, size-start);
        for (int i=start; i<stop; i++) {
            //for (ImagePost post : posts) {
            ImagePost post = posts.get(i);
            page = post.page;
            String image = post.pic;
            String fixedStr = image.replaceAll("127.0.0.1", "10.0.2.2");
            images.add(fixedStr);
        }
        if (stop >= size) {
            start = 0;
        } else {
            start = stop;
        }

        for (int i = images.size(); i < 16; i++)
        {
            images.add("");
        }

        String[] imageArr = new String[images.size()];
        imageArr = images.toArray(imageArr);

        GridView gridview = (GridView) findViewById(R.id.gridview2);
        gridview.setAdapter(new ViewImageAdapter(ViewStream.this, imageArr));
    }

    private final Response.Listener<String> onPostsLoaded_post = new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
            posts = Arrays.asList(gson.fromJson(response, ImagePost[].class));
            int size = posts.size();
            Log.i("PostActivity", size + " posts loaded.");
            page = posts.get(0).page;
            CurEndpoint = ENDPOINT + "?stream_name=" + name + ";status=success;page=" + page;
            fetchPosts();
            // Display the first 500 characters of the response string.
        }
    };

    private final Response.ErrorListener onPostsError = new Response.ErrorListener() {
        @Override
        public void onErrorResponse(VolleyError error) {
            Log.e("PostActivity", error.toString());
        }
    };


    //****************************************END OF NETWORKING CODE**************************************//*

    //*********************************************LOGIN CODE*********************************************//*

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        Log.d(TAG, "onConnectionFailed:" + connectionResult);
    }

    private void updateUI() {
        getSupportActionBar().setDisplayHomeAsUpEnabled(false);
        getSupportActionBar().setHomeButtonEnabled(false);
        title.setVisibility(View.VISIBLE);
        subtitle.setText("View A Stream: " + name);
        imageGrid.setVisibility(View.VISIBLE);
        //btn_sign_out.setVisibility(View.VISIBLE);
        //btn_sign_in.setVisibility(View.GONE);
        btn_upload.setVisibility(View.VISIBLE);
        btn_view_streams.setVisibility(View.VISIBLE);
    }
}


