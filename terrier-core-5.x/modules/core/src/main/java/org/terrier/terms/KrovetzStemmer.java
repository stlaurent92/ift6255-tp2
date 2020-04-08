/*
 * Terrier - Terabyte Retriever
 * Webpage: http://terrier.org
 * Contact: terrier{a.}dcs.gla.ac.uk
 * University of Glasgow - School of Computing Science
 * http://www.gla.ac.uk/
 *
 * The contents of this file are subject to the Mozilla Public License
 * Version 1.1 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS"
 * basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
 * the License for the specific language governing rights and limitations
 * under the License.
 *
 * Use of krovetz python module : https://github.com/ptorrestr/py_krovetz
 * By Pablo Torres <pablo.torres.t@gmail.com>
 *
 * Contributor(s):
 *   Lucas Pagès - <lucas.pages@umontreal.ca>
 */
package org.terrier.terms;


import java.io.*;


public class KrovetzStemmer extends StemmerTermPipeline{

    /* Stemmer implementation */

    public String stem(String term) {

        String stemmed = "";

        try {
            Process p = Runtime.getRuntime().exec("python3 krovetz_stem.py " + term);
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            stemmed = in.readLine();
        }catch (IOException e){
            System.out.println("IO Exception while reading the term " + term);
        }

        return stemmed;
    }
}

