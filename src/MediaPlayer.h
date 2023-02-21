#pragma once
#ifndef MEDIAPLAYER_H
#define MEDIAPLAYER_H

#import <string>

class MediaPlayer {
public:
	string mediaType;

	MediaPlayer();
	~MediaPlayer();
	void PlayMedia();
	void StopMedia();

};

#endif