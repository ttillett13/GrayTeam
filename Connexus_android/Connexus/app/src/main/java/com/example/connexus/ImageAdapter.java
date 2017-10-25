package com.example.connexus;

import com.squareup.picasso.Picasso;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;


public class ImageAdapter extends BaseAdapter {
    private Context mContext;
   // int imageTotal = 16;
    public String[] mThumbIds;
    private String[] mThumbNames;
    private static LayoutInflater mLayoutInflater=null;

    public ImageAdapter(Context c, String[] list, String[] nameList) {
        this.mContext = c;
        this.mThumbIds = list;
        this.mThumbNames = nameList;

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
        View retval = LayoutInflater.from(parent.getContext()).inflate(R.layout.image, null);
        TextView title = (TextView) retval.findViewById(R.id.os_texts);
        ImageView image_list_icon = (ImageView)retval.findViewById(R.id.os_images);


        title.setText(mThumbNames[position]);

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