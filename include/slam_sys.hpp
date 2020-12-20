#include <ros/ros.h>
#include <ros/console.h>

#include <tf/transform_broadcaster.h>
#include <tf/tf.h>

#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <vector>
#include <algorithm>
#include <Eigen/Dense>
#include <chrono>

#include "radar_driver/RadarTracks.h"
#include "radar_driver/Track.h"

#include "opencv2/core/core.hpp"
#include "opencv2/nonfree/nonfree.hpp"

#include "radar_data.hpp"

using namespace Eigen;
using namespace std;
using namespace cv;
// used this paper https://arxiv.org/pdf/2005.02198.pdf

class SLAM{
    public:
        Radat* get_current_pose();
        SLAM();
        ~SLAM();
    private:
        // this is used for radar image sizing
        int n;
        // x_pos, y_pos, x_vel, y_vel, others???
        VectorXd pose(4);
        MatrixXd key_frame();
        float keyframe_time;
        vector<MatrixXd> key_fm_history;
        vector<KeyPoint> key_frame_points;
        vector<vector <KeyPoint>> key_fm_pts_history;
        // used for equ 3 in paper, idk what this should be set to
        auto sig_c;
        // needs to be expanded to include size
        Mat RadarPicture(vector<Radat*> data);
        // relative transform between keyframe and current frame
        MatrixXd relative_transform;

        // this computes the ego velocity of the vehicle
        Vector2f SLAM::EgoMotion(vector<Radat> data);

        // TRACKING
        // feature extraction
        vector<KeyPoint> GetKeyPoints(Mat rad_img);
        // track refrence frame
        MatrixXd GetMovemntProb(vector<KeyPoint> poi);
        // track local map
        // new keyframe decision

        // LOCAL MAPPING
        // process new keyframe
        // old map point culling
        // new map point creation
        // local bundle adjust

        // LOOP DETECTION
        // descriptior extraction
        // compute SE2
        // optimize pose graph
        // global bundle adjust

        // MAP
        // keyframes
        // map points

}