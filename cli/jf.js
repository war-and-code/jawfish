/**
 * @file Jawfish is a tool for breaking into web applications.
 *
 * Originally based on Soen Vanned's Forced Evolution, a Python program.
 * https://github.com/soen-vanned/forced-evolution
 */

 console.log('JAWFISH');
 console.log('************');

/** Prints usage descriptions to the console. */
function usage() {
    console.log('Usage:');
    console.log('TARGET = <target IP / hostname>');
    console.log('ADDR = <directory>');
    console.log('VULN_VAR = <vulnerable variable>');
    console.log('METHOD = <post/get>');
    console.log('OTHER_VARIABLES=[other variables for post/get request]');
    console.log('\t VAR1=DATA1&VAR2=DATA2');
    console.log('GOAL_TEXT=<server response indicating successful exploitation>');
    console.log('\n TARGET,ADDR,VULN_VAR,METHOD,GOAL_TEXT are required');
}

var start_time = new Date();
var OTHER_VARIABLES = {};
var GOAL_TEXT = 'KEY_DATA';

var tools = '~!@#$%^&*()_+{}|:"<>?,./;\'[]\\=-0987654321`qwertyuioplkjhgfdsa';
for (i = 0; i < 3; i++) {       tools += '$%*";\'`';        } // Used to influence creature evolution

var TARGET = '';
var ADDR = '';

var CREATURE_COUNT = 333; // This will get multiplied by 3 due to database breeding
var GENOME_LENGTH = 32;
var CULL_RATE = 0.67;
var MUTATION_RATE = 0.80;
var TIMEOUT = 0.01;

var VULN_VAR = '';

// Pool will increase to (pool_original + loaded_genomes * GENE_POOL_INFLUENCE)
var GENE_POOL_INFLUENCE = 1;
var MAX_MUTATIONS = 1;
var REQ_TOTAL = 0;

var BASE_RESPONSE = '';
var METHOD = 'get'; // Default is get, but post is allowed as well

/*** DBSTARTMARKER ***/
var DB = '';
/*** DBENDMARKER ***/

/**
 * Assigns required variables through either text input or by processing web form.
 */
function process_web_form() {
    // TODO input variables
}

/**
 * Constructor class for a Creature object.
 */
function Creature() {
    var genome = '';
    var is_alive = false;
    var score = 100;
    var m_text = {};

    this.init(args, tools) {
        this.genome = '';
        this.modified = 1;
        this.is_alive = true;

        if (args == 0) {
            this.genome = tools;
        } else {
            var tmp = args;
            console.log("Creating genome with " + tmp + " characters");
            // TODO for in range
            // for…in loop
            // random integer - lower limit (arguments/2) - upper limit (arguments)
        }

        return 0;
    }

    this.run_simulation() {
        var tmp = OTHER_VARIABLES;
        tmp[VULN_VAR] = this.genome;

        try {

            if (METHOD == 0) {
                var r;  // TODO http get request
            } else {
                var r;  // TODO http post request
            }

            REQ_TOTAL += 1;
            this.m_text['text'] = r.text;
            this.m_text['url'] = r.url;
            this.m_text['status_code'] = r.status_code;

        } catch (e) {
            // Forced Evolution ignored errors - ignoring them too for now
        }

        return self.m_text;
    }
}

// TODO create creatures

// TODO cull it

// TODO mutate

// TODO breed it

// TODO fitness function

// TODO main

// TODO load DB

// TODO save DB

// TODO last line, some common thread
