
package org.terrier.matching.models;

public class NewModel extends WeightingModel {

	public NewModel() {
		super();
	}

	public final String getInfo() {
		return "NewModel";
	}

	public double score(double tf, double docLength) {
		//TODO
		return 0.0;
	}


	public void setParameter(double _b) {
		// TODO
	}


	public double getParameter() {
	    //TODO
		return 0.0;
	}
	
}
