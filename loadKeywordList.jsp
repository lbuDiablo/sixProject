<%@ page import="java.sql.*" %>
<%@ page import="org.json.simple.JSONObject"%>
<%@ page import="org.json.simple.JSONArray"%>
<%@ page language="java" contentType="application/json; charset=UTF-8"
    pageEncoding="utf-8"%>
<% request.setCharacterEncoding("utf-8"); %>
<%
	Connection con = null;
	Statement st = null;
	ResultSet rs = null;
	JSONArray jsonArray = new JSONArray();
	
	try {
		String url = "jdbc:mysql://sixproject.cica4dx4uu4o.ap-northeast-2.rds.amazonaws.com/QnA";
	    String dbId = "sixth";
		String dbPassword = "password";
		
		
		Class.forName("com.mysql.jdbc.Driver");
		con = DriverManager.getConnection(url, dbId, dbPassword);
		System.out.println("Test");
		st = con.createStatement();
		
		rs = st.executeQuery("SELECT distinct keyword_name FROM CATEGORY;");
		System.out.println(rs.next());
		while(true) {
			String keyword_name = rs.getString("keyword_name");
			JSONObject jsonobj = new JSONObject();
			jsonobj.put("keyword_name", keyword_name);
			jsonArray.add(jsonobj);
			System.out.println(jsonArray);
			if(!rs.next()) {
				rs.close();
				System.out.println("rs closed");
				break;
			}
		}
		out.print(jsonArray);
		rs.close();
		st.close();
		con.close();
		return;
	} catch (Exception e) {
		e.printStackTrace();
	} finally {

	}
%>