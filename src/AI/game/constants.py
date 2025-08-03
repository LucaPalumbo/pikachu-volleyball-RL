# ground width */
GROUND_WIDTH = 432;
# @constant @type {number} ground half-width, it is also the net pillar x coordinate */
GROUND_HALF_WIDTH = (GROUND_WIDTH // 2) | 0; #// integer division
# @constant @type {number} player (Pikachu) length: width = height = 64 */
PLAYER_LENGTH = 64;
# @constant @type {number} player half length */
PLAYER_HALF_LENGTH = (PLAYER_LENGTH // 2) | 0; #// integer division
# @constant @type {number} player's y coordinate when they are touching ground */
PLAYER_TOUCHING_GROUND_Y_COORD = 244;
# @constant @type {number} ball's radius */
BALL_RADIUS = 20;
# @constant @type {number} ball's y coordinate when it is touching ground */
BALL_TOUCHING_GROUND_Y_COORD = 252;
# @constant @type {number} net pillar's half width (this value is on this physics engine only, not on the sprite pixel size) */
NET_PILLAR_HALF_WIDTH = 25;
# @constant @type {number} net pillar top's top side y coordinate */
NET_PILLAR_TOP_TOP_Y_COORD = 176;
# @constant @type {number} net pillar top's bottom side y coordinate (this value is on this physics engine only) */
NET_PILLAR_TOP_BOTTOM_Y_COORD = 192;

# window height */
HEIGHT = 304;

# /**
#  * It's for to limit the looping number of the infinite loops.
#  * This constant is not in the original machine code. (The original machine code does not limit the looping number.)
#  *
#  * In the original ball x coord range setting (ball x coord in [20, 432]), the infinite loops in
#  * {@link calculateExpectedLandingPointXFor} function and {@link expectedLandingPointXWhenPowerHit} function seems to be always terminated soon.
#  * But if the ball x coord range is edited, for example, to [20, 432 - 20] for left-right symmetry,
#  * it is observed that the infinite loop in {@link expectedLandingPointXWhenPowerHit} does not terminate.
#  * So for safety, this infinite loop limit is included for the infinite loops mentioned above.
#  * @constant @type {number}
#  */
INFINITE_LOOP_LIMIT = 1000;


WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)