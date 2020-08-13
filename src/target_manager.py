from target import *
from math import *

# THIS CLASS MANAGES ALL OF THE TARGETS 
class TargetManager:
    def __init__(self):
        # super().__init__()
        # a list of active targets
        self.active_targets = []

    # take in raw tracks and add to existing target or create new target
    # more of a callback
    def update(self, tracks):
        stragglers = self.grouper(tracks)
        # probability of each centroid going to each target
            # check for conflicts


    # This creates the selection criteria for divvying up the tracks for tracks
    def selection_criteria(self, sorted_tracks):
        if sorted_tracks < 80: 
            return # something bad

        # uhhh get some top percentage of tracks
        ten_percent = len(sorted_tracks)//10
        # This needs work and should be something smarter
        # get the best points
        # look at the data maybe?

        return sorted_tracks[:ten_percent]


    # This looks for groups of targets
    # USE DISTANCE AND VELOCITY TO GROUP
    def grouper(self, tracks):
        usable_tracks = tracks
        # if there are no active targets make new ones based on data
        if(len(self.active_targets) != 0):
            for target in self.active_targets:
                probabilities = self.distanceTo(target.current_pose, usable_tracks)
                # something = 2 # YOU NEED TO DETERMINE THE METRIC BASED ON THE DATA
                # candidate_tracks = [p for p in proabilities if p.prob >= something]
                candidate_tracks = self.selection_criteria(probabilities)
                # YOU NEED TO FIGURE OUT SOMETHING BETTER FOR THE dt THERE
                target.updateTarget(candidate_tracks, 0.1)
                # Remove tracks used for this target
                usable_tracks = list(set(usable_tracks)^set(candidate_tracks))
            
        # Go through what remians and find more targets until random noise is left
        left_overs = self.findNewTargets(usable_tracks)

        # These are the stragglers
        return usable_tracks


    # retuens a sorted list of probabilities of every other point being part of the same targets as the starting point
    def distanceTo(self, point, tracks):
        distances = []
        for track in tracks:
            new_del = Delta(point, track).prob
            distances.append((track, new_del))
            

        sorted_distances = sorted(distances, key=lambda relation: relation[1], reverse=True)
        sorted_distances = [ x[0] for x in sorted_distances]
        print(sorted_distances)
        return sorted_distances


    # This finds new targets in the data
    def findNewTargets(self, usable_tracks):
        for track in usable_tracks:
            probabilities = self.distanceTo(track, usable_tracks)
            # something = 2 # YOU NEED TO DETERMINE THE METRIC BASED ON THE DATA
            # probable_tracks = [p for p in probabilities if p.prob >= something]
            candidate_tracks = self.selection_criteria(probabilities)
            new_target = Target(candidate_tracks)
            # Remove the tracks for the new target from the list
            usable_tracks = list(set(usable_tracks)^set(candidate_tracks))
            self.active_targets.append(new_target)
        return usable_tracks
        



class Delta:
    def __init__(self, track1, track2):
        self.track1 = track1
        self.track2 = track2
        self.dx = abs(self.track1.cart_x - self.track2.cart_x)
        self.dy = abs(self.track1.cart_y - self.track2.cart_y)
        self.dvx = abs(self.track1.rate_x - self.track2.rate_x)
        self.dvy = abs(self.track1.rate_y - self.track2.rate_y)
        self.dist = sqrt(self.dx**2 + self.dy**2)
        self.vel_del = sqrt(self.dvx**2 + self.dvy**2)
        self.prob = self.probability()
    
    # This calculates the probability of the two points being part of the same target
    def probability(self):
        # THIS IS TRASH AND NEEDS TO BE BETTER
        # less of a distace delta means a higher probability
        p_dis = 1/((self.dist + 0.0001)**1.0)
        # lower velocity delta means a higher probability 
        p_vel = 1/((self.vel_del + 0.0001)**1.0)
        # This changes how much of the metric is based on distance
        dist_mult = 1
        # This changes how much of the metric is based on velocity
        vel_mult = 1

        return (p_dis * dist_mult) * (p_vel * vel_mult)
