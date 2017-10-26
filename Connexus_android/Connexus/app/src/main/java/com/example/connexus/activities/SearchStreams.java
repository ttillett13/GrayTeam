package com.example.connexus.activities;


import android.content.Context;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.Html;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.GridView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.connexus.ImageAdapter;
import com.example.connexus.MainActivity;
import com.example.connexus.R;
import com.example.connexus.StreamPost;
import com.example.connexus.beans.SearchStreamModel;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.List;

public class SearchStreams extends AppCompatActivity{
    private Context mContext;
    private static final String TAG = MainActivity.class.getSimpleName();
    private Gson gson;
    private List<SearchStreamModel> posts;


    private TextView tv_SearchResult;
    private GridView gv_allStreams;
    private Button btn_Search, btn_MoreResult;
    private EditText et_Search;
    //public static final String BASE_ENDPOINT = "https://vibrant-mind-177623.appspot.com/";
    //private static final String ENDPOINT = BASE_ENDPOINT + "ViewSingleStream/api";

    private static final String ENDPOINT = "http://10.0.2.2:8080/SearchStream/api";
    private String CurEndpoint;

    private RequestQueue requestQueue;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.search_streams);

        tv_SearchResult = (TextView) findViewById(R.id.tv_SearchResult);
        gv_allStreams = (GridView) findViewById(R.id.gv_allStreams);;
        btn_Search = (Button) findViewById(R.id.btn_Search);;
        btn_MoreResult = (Button) findViewById(R.id.btn_MoreResult);;
        et_Search = (EditText) findViewById(R.id.et_Search);

//        tv_SearchResult.setVisibility(View.GONE);
//        btn_MoreResult.setVisibility(View.GONE);

        String searchText = getIntent().getStringExtra("query").trim();
        et_Search.setText(searchText);

        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.setDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSSSSS");
        gson = gsonBuilder.create();

        requestQueue = Volley.newRequestQueue(this);
        if(searchText.length() > 0){
            CurEndpoint = ENDPOINT + "?search=" + searchText;
            fetchPosts();
        }
       // processGridData();
       // fillData();

        btn_Search.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                posts=null;
               // fillData();
                processGridData();
            }
        });
        btn_MoreResult.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                posts=null;
                //fillData();
                processGridData();
            }
        });
    }

    /*******************************************NETWORKING CODE******************************************/
    private void fetchPosts() {
        StringRequest request = new StringRequest(Request.Method.GET, CurEndpoint, onPostsLoaded, onPostsError);
        requestQueue.add(request);
    }

    private final Response.Listener<String> onPostsLoaded = new Response.Listener<String>() {
        @Override
        public void onResponse(String response) {
            posts = Arrays.asList(gson.fromJson(response, SearchStreamModel[].class));

            processGridData();
        }
    };

    private final Response.ErrorListener onPostsError = new Response.ErrorListener() {
        @Override
        public void onErrorResponse(VolleyError error) {
            Log.e("PostActivity", error.toString());
        }
    };

    private SearchStreamModel getDummyData(int rndNo){
        SearchStreamModel ssm = new SearchStreamModel();
        ssm.datetime = Calendar.getInstance().getTime();
        ssm.name = "Name - "+rndNo;
        ssm.path = "/ViewSingleStream?stream_name=Nature Stream";
        ssm.url =  "http://127.0.0.1:8080/_ah/img/encoded_gs_file:c3RhZ2luZy52aWJyYW50LW1pbmQtMTc3NjIzLmFwcHNwb3QuY29tL1BpY3R1cmVzL0tvYWxhLmpwZw==";
        return ssm;
    }
    private void processGridData(){

        if(posts==null || posts.size()==0){
            Toast.makeText(this, "No Record Found!", Toast.LENGTH_SHORT).show();
            return;

        }
        tv_SearchResult.setText(Html.fromHtml(getString(R.string.search_result,posts.size()+"", "\""+et_Search.getText().toString().trim()+"\"")));
        ArrayList<String> images = new ArrayList<String>();
        ArrayList<String> names = new ArrayList<String>();

        Log.i("PostActivity", posts.size() + " posts loaded.");
        for (SearchStreamModel post : posts) {
            String fixedStr;
            fixedStr = post.url.replaceAll("127.0.0.1", "10.0.2.2");
            images.add(fixedStr);
            names.add(post.name);
        }

//        for (int i = 0; i < 16; i++)
//        {
//            images.add("");
//            names.add("");
//        }

        String[] imageArr = new String[images.size()];
        imageArr = images.toArray(imageArr);
        String[] nameArr = new String[names.size()];
        nameArr = names.toArray(nameArr);


        gv_allStreams.setAdapter(new ImageAdapter(SearchStreams.this, imageArr, nameArr));
    }
    private void fillData(){
        if(posts==null || posts.size()==0) {

            posts = new ArrayList<>();
        }
            for (int i = 0; i < 8; i++) {
                posts.add(getDummyData(i));
            }
            processGridData();

    }
}

