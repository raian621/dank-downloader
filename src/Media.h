#pragma once
#ifndef MEDIA_H
#define MEDIA_H

#import "MediaData.h"
#import "MediaPlayer.h"
#import <string>

class Media {
public: 
	unsigned int playbackLength;
	string mediaURL;
	string filePath;
	MediaData mediaData;
	MediaPlayer mediaPlayer;
};

#endif