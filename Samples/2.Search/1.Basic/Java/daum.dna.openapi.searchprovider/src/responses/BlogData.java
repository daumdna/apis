package responses;

import java.util.ArrayList;

public class BlogData {
	private String title;
	private String link;
	private String description;
	private String lastBuildDate;
	private int totalCount;
	private int pageCount;
	private int result;
	private ArrayList<BlogItemData> items = new ArrayList<BlogItemData>();
	
	public String toString()
	{
		String outStr = "";
		outStr += "title" + ":" + title + "\n";
		outStr += "link" + ":" + link + "\n";
		outStr += "description" + ":" + description + "\n";
		outStr += "lastBuildDate" + ":" + lastBuildDate + "\n";
		outStr += "totalCount" + ":" + totalCount + "\n";
		outStr += "pageCount" + ":" + pageCount + "\n";
		outStr += "result" + ":" + result + "\n";
		outStr += "itemsCount" + ":" + items.size() + "\n\n";
		
		for(int i=0;i < getItems().size();i++)
		{
			outStr += "item(" + i + ")\n";
			outStr += "item(" + i + ") title:" + items.get(i).getTitle() + "\n";
			outStr += "item(" + i + ") link:" + items.get(i).getLink() + "\n";
			outStr += "item(" + i + ") description:" + items.get(i).getDescription() + "\n";
			outStr += "item(" + i + ") comment:" + items.get(i).getComment() + "\n";
			outStr += "item(" + i + ") author:" + items.get(i).getAuthor() + "\n";
			outStr += "item(" + i + ") pubDate:" + items.get(i).getPubDate() + "\n\n";
		}
		return outStr;
	}
	
	/**
	 * @param Title the Title to set
	 */
	public String getTitle()
	{
		return this.title;
	}
	
	/**
	 * @param Title the Title to set
	 */
	public void setTitle(String title) {
		this.title = title;
	}

	/**
	 * @param link the link to set
	 */
	public void setLink(String link) {
		this.link = link;
	}

	/**
	 * @return the link
	 */
	public String getLink() {
		return link;
	}

	/**
	 * @param description the description to set
	 */
	public void setDescription(String description) {
		this.description = description;
	}

	/**
	 * @return the description
	 */
	public String getDescription() {
		return description;
	}

	/**
	 * @param lastBuildDate the lastBuildDate to set
	 */
	public void setLastBuildDate(String lastBuildDate) {
		this.lastBuildDate = lastBuildDate;
	}

	/**
	 * @return the lastBuildDate
	 */
	public String getLastBuildDate() {
		return lastBuildDate;
	}

	/**
	 * @param totalCount the totalCount to set
	 */
	public void setTotalCount(int totalCount) {
		this.totalCount = totalCount;
	}

	/**
	 * @return the totalCount
	 */
	public int getTotalCount() {
		return totalCount;
	}

	/**
	 * @param pageCount the pageCount to set
	 */
	public void setPageCount(int pageCount) {
		this.pageCount = pageCount;
	}

	/**
	 * @return the pageCount
	 */
	public int getPageCount() {
		return pageCount;
	}

	/**
	 * @param result the result to set
	 */
	public void setResult(int result) {
		this.result = result;
	}

	/**
	 * @return the result
	 */
	public int getResult() {
		return result;
	}

	/**
	 * @return the items
	 */
	public ArrayList<BlogItemData> getItems() {
		return items;
	}
}
