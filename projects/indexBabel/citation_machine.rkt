#lang racket
(require db)

;----------Versioning----------;

(define VERSION 0.01)
(define not-yet-supported 
  "\t1. Multiple Authors
\t2. Journal editions
\t3. Translators
\t4. Page Ranges
\t5. itallic vs quoted
\t   formatting for titles
\t6. Non-print Sources\n\n\n")

;----------Source Data Fields----------------;

(define book '("id" "title" "volume" "edition" "authors" 
               "translator" "publisher" "city" "state" 
               "country" "year"))

(define article '("id" "title" "volume" "page_number" 
                  "authors" "translator" "magazine_or_website" 
                  "url" "location" "data_published" "date_accessed"))

(define performance '("id" "title" "director" "screen_writer" 
                      "performers" "distributor" "city" "country" 
                      "date" "meduim"))

;----------SQL connection Functions----------;

(define start-connection
  #| Returns an active 
     database connection |#
  (λ ()
    (let ([connection '()])
      (and (printf "Starting...") 
           (if (sqlite3-available?)
               (set! connection 
                     (sqlite3-connect #:database "citation_catalog"
                                      #:mode 'create))
               (printf "FAILURE: SQLite3 resources not found!\n"))
           (printf "Connecting...")
           (if (connected? connection)
               (printf "Connected!\n\n\n")
               (printf "Failure! Connection could not be made.\n")))
      connection)))

;----------set-up functions----------;

(define main
   (λ ()
     (define catalog (start-connection))
     (create-table catalog)
     (welcome)
     (directory catalog)
     (printf "Good bye!\n")))

(define create-table                                                              ;;;test
  #| If a table does not exist in 'connection' once is created.    |#
  (λ (connection)                                                                         
    (query-exec connection 
                "CREATE TABLE IF NOT EXISTS books( id TEXT,
                                                   title TEXT,
                                                   volume TEXT,
                                                   edition TEXT
                                                   authors TEXT,
                                                   translator TEXT,
                                                   publisher TEXT,
                                                   city TEXT,
                                                   state TEXT
                                                   country TEXT,
                                                   year TEXT)") ;;none stores values: page numbers, chapter title
    (query-exec connection 
                "CREATE TABLE IF NOT EXISTS article( id TEXT,
                                                     title TEXT,
                                                     volume TEXT,
                                                     page_number TEXT
                                                     authors TEXT,
                                                     translators TEXT,
                                                     magazine_or_website TEXT,
                                                     url TEXT,
                                                     location TEXT,
                                                     date_published TEXT,
                                                     date_accessed TEXT)") ;;date format M/D/Y
    (query-exec connection 
                "CREATE TABLE IF NOT EXISTS performance( id TEXT,
                                                         title TEXT,
                                                         director TEXT,
                                                         screen_writer TEXT,
                                                         performers TEXT,
                                                         distributors TEXT,
                                                         city TEXT,
                                                         country TEXT,
                                                         date TEXT,
                                                         meduim TEXT)")))

(define directory
  (λ (connection)
    (printf "Please choose and option by typing it below:
                                      1. cite an entry.
                                      2. add an entry.
                                      3. exit.\n")
    
    (define action (read-line))
    (and
     (cond 
      [(or (equal? action "cite an entry") (equal? action "1"))
       (format-citation connection)]
      [(or (equal? action "add an entry") (equal? action "2"))
       (add-entry connection)]
      [(or (equal? action "exit") (equal? action "3"))
       false]
      [else (printf "I am sorry, I don't know that command.\n") 
            (directory connection)])
    (directory connection))))

(define welcome
  (λ ()
    (printf 
     "Hello and Welcome to E.C.H.O.S.,
an Electronic Citation Helper &
Organizer System, version ~a!
-----------------------------------------
Use this tool to organize, store, and 
format any citation you could need 
(other than those not yet implemented).
If you have any problems or run into
any bugs, contact Logan. Enjoy!

Programmer: Logan Davis
Contact info: ldavis@marlboro.edu
-----------------------------------------
NOT YET SUPPORTED:\n~a
-----------PROMPT STARTING -------------\n"
     VERSION
     not-yet-supported)))

;----------SQLite query functions----------;

(define get-info                                                                   ;;;make
  #| Asks the user for all information relevant for a 
     proper citation and returns a list of  answers.   |#
  (λ (source-type)
    (define entries '())
    (define entry-fields
      (cond
        [(equal? source-type "book") book]
        [(equal? source-type "article") article]
        [(equal? source-type "performance") performance]))
    (for ([i entry-fields])
      (printf "please enter the ~a \n" i)
      (set! entries (append entries (list (read-line)))))
    entries))


(define add-entry                                                                  ;;;fix
  #| adds a given work to the collection of 
     citable materials saved on 'connection'. |#
  (λ (connection)
    (printf "What kind of source are you citing?\n")
    (define type-of-entry (read-line))
    (define hash-entry (vector->input-hash (get-info type-of-entry) type-of-entry))
    (query-exec connection 
                "INSERT INTO citation_info VALUES ($1,$2,$3,$4,$5)" 
                (hash-ref hash-entry "title")
                (hash-ref hash-entry "author")
                (hash-ref hash-entry "publisher")
                (hash-ref hash-entry "location")
                (hash-ref hash-entry "date"))))
  
      
(define inquery                                                                    ;;;TEST
  (λ (connection)
    #| Asks the user for what kind of work and the title of the work 
       they wish to cite.  Uses the answer to make a query to 'connection'.
       Returns a hash-table and set of keys of the queried data             |#
    (printf "What kind of source are you wishing to cite:
     1. Book (EG a novel, test book, memior, or dictionary)
     2. Article (EG a journal peice, web page, or a magazine story)
     3. Performance (EG Plays and films)\n")
    (define action (string-downcase (read-line)))
    (printf "What was the title of the work you are citing?\n")
    (define request (string-downcase (read-line)))
    (define response 
      (query-row connection "SELECT * FROM $1 WHERE id = $2" action request))
    (vector->input-hash response action)))

;----------General Helper Functions----------;

(define pretty-table
  (λ (hash-entry)
    (printf "--------INFO----------------------------------------------------
| Title       | ~a 
------------------------------------------------------------------
| Author      | ~a 
------------------------------------------------------------------
| Publisher   | ~a 
------------------------------------------------------------------
| Location of | ~a 
| Publisher   | ~a
------------------------------------------------------------------
| Date of     | ~a
| Publication | ~a"))) ;;;FINISH THIS!!!



(define vector->input-hash                                                        ;;;TEST
  #| Turns 'vec' into a hash-table of information
     defined by 'action' to be used for citations.           |#
  (λ (vec action)
    (define keys 
      (cond 
      [(equal? action "book") book]
      [(equal? action "article") article]
      [(equal? action "performance") performance]))
    (define collected-data (make-hash))
    (for ([value vec] [key keys])
      (hash-set! collected-data key value))
    collected-data))

(define name-switcher
  ;;TODOS:
  ;; allow middle initials
  (λ (name)
    (define name-list (string-split name))
    (string-append (last name-list) ", " (first (reverse (rest (reverse name-list)))))))

;----------Citation Formmating Functions----------;                                         ;;;REDO EVERYTHING

(define format-citation
  #| Finds out which work the user wishes to cite and than 
     prompts them for which citation format they wish to use.
     Depending to their  answer on the latter,
     the corresponding format-function will be called.
     This function only needs to be passed  the connection to the 
     Database.                                                    |#
  (λ (connection)
    (define info (inquery connection))
    (define citation-data (last info))
    (define medium (first info))
    (printf "Which Citation Format would you like (Chicago, MLA, or APA)?\n")
    (define action (string-upcase (read-line)))
    (cond 
      [(equal? action "MLA") (mla citation-data medium)]
      [(equal? action "APA") (apa citation-data medium)]
      [(equal? action "CHICAGO") (chicago citation-data medium)])))

(define mla 
  (λ (hash-entry)
    (printf "In-Line Formatting:\n (~a 'page number')\n"
            (last (string-split (hash-ref hash-entry "author"))))
    (printf "Bibliography Formatting:\n ~a. ~a. ~a: ~a, ~a.\n\n"
            (name-switcher (hash-ref hash-entry "author"))
            (hash-ref hash-entry "title")
            (hash-ref hash-entry "location")
            (hash-ref hash-entry "publisher")
            (hash-ref hash-entry "date"))))

(define apa 
  (λ (hash-entry)
    (printf "In-Line Formatting:\n (~a, ~a,'page numbers')\n"
            (hash-ref hash-entry "author")
            (hash-ref hash-entry "date"))
    (printf "Bibliography Formatting:\n ~a.(~a). ~a. ~a.\n\n"
            (name-switcher (hash-ref hash-entry "author"))
            (hash-ref hash-entry "date")
            (hash-ref hash-entry "title")
            (hash-ref hash-entry "publisher"))))

(define chicago
  (λ (hash-entry)
    (printf "Foot Note Formatting:\n ~a. ~a (~a: ~a, ~a), 'page numbers'.\n"
            (hash-ref hash-entry "author")
            (hash-ref hash-entry "title")
            (hash-ref hash-entry "location")
            (hash-ref hash-entry "publisher")
            (hash-ref hash-entry "date"))
    (printf "Bibliography Formatting:\n ~a. ~a. ~a: ~a, ~a.\n\n"
            (name-switcher (hash-ref hash-entry "author"))
            (hash-ref hash-entry "title")
            (hash-ref hash-entry "location")
            (hash-ref hash-entry "publisher")
            (hash-ref hash-entry "date"))))
