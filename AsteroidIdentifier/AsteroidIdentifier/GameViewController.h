//
//  GameViewController.h
//  AsteroidIdentifier
//
//  Created by Abdul Al-Shawa on 2016-04-23.
//  Copyright (c) 2016 Abdul Al-Shawa. All rights reserved.
//

#import <SceneKit/SceneKit.h>
#import <QuartzCore/QuartzCore.h>
#import <CorePlot/CorePlot.h>

#import "GameView.h"

@interface GameViewController : NSViewController <NSTableViewDelegate, NSTableViewDataSource, CPTPlotDataSource>

@property (assign) IBOutlet GameView *gameView;
@property (weak) IBOutlet NSTableView *asteroidTableView;
@property (weak) IBOutlet CPTGraphHostingView *graphHostView;

@end