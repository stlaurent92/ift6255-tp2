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
 * The Original Code is ApplyTermPipeline.java.
 *
 * The Original Code is Copyright (C) 2017-2020 the University of Glasgow.
 * All Rights Reserved.
 *
 * Contributor(s):
 *  Craig Macdonald
 */
package org.terrier.querying;

import java.util.Iterator;

import gnu.trove.TIntArrayList;

import org.terrier.matching.MatchingQueryTerms;
import org.terrier.matching.MatchingQueryTerms.MatchingTerm;
import org.terrier.matching.matchops.MultiTermOp;
import org.terrier.matching.matchops.Operator;
import org.terrier.matching.matchops.SingleTermOp;
import org.terrier.terms.BaseTermPipelineAccessor;
import org.terrier.terms.TermPipelineAccessor;
import org.terrier.utility.ApplicationSetup;

@ProcessPhaseRequisites(ManagerRequisite.MQT)
public class ApplyTermPipeline implements Process {

	TermPipelineAccessor tpa = null;
	String info = null;
	
	public ApplyTermPipeline()
	{
		this.load_pipeline();
	}
	
	/** load in the term pipeline */
	protected void load_pipeline()
	{
		final String tp = ApplicationSetup.getProperty("termpipelines", "Stopwords,PorterStemmer").trim();
		final String[] pipes = tp.split("\\s*,\\s*");
		info = "termpipelines=" + tp;
		synchronized (this) {
			tpa = new BaseTermPipelineAccessor(pipes);
		}		
	}
	
	interface Visitor {
		boolean visit(Operator qt);
		boolean visit(SingleTermOp sqt);
		boolean visit(MultiTermOp mqt);
	}
	
	
	
	@Override
	public void process(Manager manager, Request q) {
		
		
		TIntArrayList toDel = new TIntArrayList();
		int i=-1;
		
		Visitor visitor = new Visitor()
		{
			@Override
			public boolean visit(Operator qt) {
				if(qt instanceof SingleTermOp)
				{
					return this.visit((SingleTermOp)qt);
				}
				else if(qt instanceof MultiTermOp)
				{
					return this.visit((MultiTermOp)qt);
				}
				return true;
			}
			
			@Override
			public boolean visit(SingleTermOp sqt) {
				String origTerm = sqt.getTerm();
				String newTerm = tpa.pipelineTerm(origTerm);
				if (newTerm == null)
					return false;
				sqt.setTerm(newTerm);
				return true;
			}

			@Override
			public boolean visit(MultiTermOp mqt) {
				Operator[] qts = mqt.getConstituents();
				boolean OK = true;
				for(Operator qt : qts) {
					//boolean OKqt = 
					this.visit(qt);
				}
				//TODO check if all required?
				return OK;
			}
			
		};
		
		MatchingQueryTerms mqt = q.getMatchingQueryTerms();
		String lastTerm = null;
		boolean dups = false;
		for(MatchingTerm t : mqt)
		{
			i++;
			boolean OK = visitor.visit(t.getKey());
			if (! OK)
				toDel.add(i);
			else
			{
				dups = dups || (t.getKey().toString().equals(lastTerm));
				lastTerm = t.getKey().toString();
			}
		}
		toDel.reverse();
		for(int removeIndex : toDel.toNativeArray())
		{
			mqt.remove(removeIndex);
		}
		
		if (! dups)
			return;
		
		MatchingTerm prev = null;
		Iterator<MatchingTerm> iter = mqt.iterator();
		while(iter.hasNext())
		{
			MatchingTerm t = iter.next();
			if (prev != null 
					&& t.getKey().toString().equals(prev.getKey().toString())  // this and the previous have the same string
					&& t.getValue().equals(prev.getValue()) // this previous word has the same models, tags and requirements
					)
			{
				prev.getValue().setWeight(prev.getValue().getWeight() + t.getValue().getWeight());
				iter.remove();
			}
			prev = t;
		}
	}

	@Override
	public String getInfo() {
		return this.getClass().getSimpleName() + '(' + this.info + ')';
	}

}
