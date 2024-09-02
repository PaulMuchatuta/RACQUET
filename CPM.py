import nltk
import sys

#nltk.download('punkt') #haveto download punkt again for some reason.
from nltk.tokenize import sent_tokenize, word_tokenize, TweetTokenizer
#from nltk.corpus import brown #nltk test, comment out once working
#nltk.download('brown') #haveto download punkt again for some reason.
#print(brown.words())
#nltk.download('averaged_perceptron_tagger')

def Comparative_Parsing_Module(User_Input):
    #//CONTEXT FREE GRAMMAR MODULE\\#
    #simple Context free grammar rules based on NLTK Book https://www.nltk.org/book/ch08.html.
    #1. Sentence(S) made of Noun Phrase (NP) and Verb Phrase (VP), 2. VP made up of Verb(V) NP OR V NP Prepositional Phrase(PP),
    #3. Verbs, 4. Noun phrases such as Proper Noun(N) OR Determinant(D) N OR D N PP, 5. D such as a, an, the, 6. nouns such as system
    #7. prepositioners such as in on by with, #8. KEY: Modal and Auxilliary, e.g. CanNOT) such as shall OR Must OR Will OR should
    #Penn Tree Back POS library used https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    #adding state driven EARS paths for "While there is no card, the system shall execute order 66". Complete.
    grammar = nltk.CFG.fromstring("""
    S -> NP VP | STA NP VP
    NP -> NN | NN NN | DT NN | DT NN PP | NN CD
    VP -> VB NP | VB NP PP | MD VP | MD VB P NP | P NP
    STA -> P EX VBZ DT NN P DT NN SYM | P EX VBZ DT NN SYM | P 
    PP -> P NP
    CC -> "for" | "and" | "nor" | "but" | "or" | "yet" | "so"
    CD -> "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "10" | "11" | "12" | "13" | "14" | "15" | "16" | "17" | "18" | "19" | "20" | "21" | "22" | "23" | "24" | "25" | "26" | "27" | "28" | "29" | "30" | "31" | "32" | "33" | "34" | "35" | "36" | "37" | "38" | "39" | "40" | "41" | "42" | "43" | "44" | "45" | "46" | "47" | "48" | "49" | "50" | "51" | "52" | "53" | "54" | "55" | "56" | "57" | "58" | "59" | "60" | "61" | "62" | "63" | "64" | "65" | "66" | "67" | "68" | "69" | "70" | "71" | "72" | "73" | "74" | "75" | "76" | "77" | "78" | "79" | "80" | "81" | "82" | "83" | "84" | "85" | "86" | "87" | "88" | "89" | "90" | "91" | "92" | "93" | "94" | "95" | "96" | "97" | "98" | "99" | "100" 
    DT -> "a" | "an" | "the" | "my" | "no"
    EX -> "there"
    FW -> 
    P -> "in" | "on" | "by" | "with" | "while" | "when"
    JJ -> "large" | "accurate" | "clear" | "essential" | "explicit" | "feasible" | "flexible" | "measurable" | "necessary" | "precise" | "specific" | "valid" | "robust" | "User-friendly" | "sustainable" | "reliable" | "efficient" | "durable" | "adaptable" | "functional" | "safe" | "responsive" | "secure" | "effective" | "compact" | "passenger-centric" | "maintainable" | "available" | "high-speed" | "high speed" | "multimodal" | "electrified" | "interconnected" | "punctual" | "integrated" | "comfortable" | "stratospheric" | "mission-oriented" | "global" | "cost-effective" | "cost effective" | "exploratory" | "mission-critical" | "interdisciplinary" | "multidisciplinary" | "strategic" | "collaborative" | "cutting-edge"
    JJR -> "larger"              
    JJS -> "Largest"
    LS -> 
    MD -> "can" | "cannot" | "could" | "couldn't" | "dare" | "may" | "might" | "must" | "need" | "ought" | "shall" | "should" | "shouldn't" | "will" | "would"                             
    NN -> "system" | "subsystem" | "order" | "card" | "atm" | "radar" | "satellite" | "groundstation" | "boom" | "conflict"
    VB -> "execute" | "interface" | "be" | "uplink" | "extend" | "downlink" | "communicate" 
    VBZ -> "is" | "are"
    SYM -> "!" | "(" | ")" | '"' | "'" | "£" | "$" | "%" | "^" | "&" | "*" | "-" | "_" | "+"  | "=" | "[" | "]" | "{" | "}" | "~" | "#" | ":" | "?" | "." | ","
    """)
    #print(User_Input)
    requirement = User_Input #FIND FIX FOR THE GRAMMAR CASE ISSUE

    def CFG_From_String():
        try:
            strippedrequirement=requirement.casefold().replace(",", " ,").split()
            #print (strippedrequirement)
            rd_parser = nltk.RecursiveDescentParser(grammar) #tree diagram parser
            collect_p=""
            #iterate parse trees
            for p in rd_parser.parse(strippedrequirement):
                #print(p) #print parse tree - TEST
                collect_p +=str(p) #collect p print outs until loop completes, appending on end of collect_p
            
            if not collect_p.strip():
                CFGFS="No valid parse found."
            else:
                CFGFS=(f"CFG: {collect_p}")
            return CFGFS
        except Exception:
            #print()
            CFGFS="CFG: The entered requirement is outside the constraints of the Context Free Grammar library. Please refer to the AI module which is better suited to complex and unstructured requirements."
            return CFGFS

    CFGFS=CFG_From_String()

    #//CONTEXT FREE GRAMMAR MODULE - If loops for standard requirement rules flags\\#

    #//POS TAGGING AND TRAINING\\ #Part-of-speech(POS)tagging - grammatically training the programme
    def POS_Tagging():
        try:
            text = nltk.word_tokenize(requirement)
            list_of_tokens = nltk.pos_tag(text)
            #print(f"POS: {list_of_tokens}")
            LOT=(f"POS: {list_of_tokens}")
            return LOT
        except Exception:
            #print()
            LOT="POS: The entered requirement is outside the constraints of the Part of Speech tagging. Please refer to the AI module which is better suited to complex and unstructured requirements."
            return LOT
 

    LOT=POS_Tagging()
    #sentences=word_tokenize(requirement) # tokenise seperately to allow single token. commented out as not adding much 

    #//MULTI-SENTENCE ANALYSIS\\#
    def Multi_Sentence_Analysis():
        try:
            tokenizer_words = TweetTokenizer() #tweettokenizer more attuned to human language and used on tweets. Less sensitive to word case changes, thereby less sesnitive to unstrtuctured human speech
            tokens_sentences = [tokenizer_words.tokenize(t) for t in #initialise for loop to go through each item in string
            nltk.sent_tokenize(requirement)] #sent_tokenize to begin splitting the words into tokens
            #print(f"MSA:{tokens_sentences}") #print multi sentence
            MSA=(f"MSA:{tokens_sentences}")
            #print(tokenizer_words.tokenize(requirement)[1]) #print single word
            return MSA
        except Exception:
            MSA="MSA: The entered requirement is outside the constraints of the Multi-Sentence Analysis. Please refer to the AI module which is better suited to complex and unstructured requirements."
            return MSA

    MSA=Multi_Sentence_Analysis()
    #rules output. If possible, see if this can be added into the OpenAI prompt. DOES NOT WORK YET
    #def Rules_check(): 
        #while true:
        #    if requirement output contains "shall":
        #        if requirment output does not contain more than one "shall"
        #            if etc
        #        else 
        #            print("this requirement appears to be multiple requirements")
        #    elif requirement does not contain "Shall"
        #        print("This requirement does not contain a word like 'shall' to determine what must be performed")
    #Comparative_Parsing_Module() - comment back in when just testing this

    return CFGFS, LOT, MSA

def main(): 
    if len(sys.argv)<2:
        print("no input returned")
        return
    
    requirement = sys.argv[1]
    CFGFS, LOT, MSA = Comparative_Parsing_Module(requirement)
    #print(result)
    print(f"Results are as follows: {CFGFS}\n{LOT}\n{MSA}\n\nThe following rules should be reviewed: ")

if __name__=="__main__":
    main()
