package com.example.connexus;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;


public class NearbyImageAdapter extends BaseAdapter {
    private Context mContext;
   // int imageTotal = 16;
    public String[] mThumbIds;
    private String[] mThumbNames;
    private String[] mThumbDistance;
    private static LayoutInflater mLayoutInflater=null;

    public NearbyImageAdapter(Context c, String[] list, String[] nameList, String[] distanceList) {
        this.mContext = c;
        this.mThumbIds = list;
        this.mThumbNames = nameList;
        this.mThumbDistance=distanceList;

        mLayoutInflater = ( LayoutInflater )c.
                getSystemService(Context.LAYOUT_INFLATER_SERVICE);
    }

    public int getCount() {
        return mThumbNames.length;
    }

    @Override
    public String getItem(int position) {
        return mThumbIds[position];
    }

    public long getItemId(int position) {
        return 0;
    }

    public View getView(int position, View convertView, ViewGroup parent) {
        View retval = LayoutInflater.from(parent.getContext()).inflate(R.layout.nearby_image, null);
        TextView title = (TextView) retval.findViewById(R.id.os_texts);
        ImageView image_list_icon = (ImageView)retval.findViewById(R.id.os_images);
        TextView distance = (TextView) retval.findViewById(R.id.os_texts_distance);


        title.setText(mThumbNames[position]);
        distance.setText(mThumbDistance[position]);

        String url = getItem(position);
        int length = url.length();
        if (length > 0) {
            Picasso.with(retval.getContext()).load(url).fit().centerCrop().into(image_list_icon);
        }
        else if (mThumbNames[position].length() > 0){
            Picasso.with(retval.getContext()).load("http://placehold.it/150").fit().centerCrop().into(image_list_icon);
        }
        return retval;
    }
}