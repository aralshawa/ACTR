//
//  AsteroidCellView.h
//  AsteroidIdentifier
//
//  Created by Abdul Al-Shawa on 2016-04-23.
//  Copyright © 2016 Abdul Al-Shawa. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface AsteroidCellView : NSTableCellView

@property (weak) IBOutlet NSImageView *asteroidImageView;
@property (weak) IBOutlet NSTextField *asteroidNameLabel;
@property (weak) IBOutlet NSTextField *asteroidIDLabel;

@end
