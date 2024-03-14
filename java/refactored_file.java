/*
 * Copyright (C) 1999-2015 Jive Software. All rights reserved.
 *
 * This software is the proprietary information of Jive Software. Use is subject to license terms.
 */
package com.jivesoftware.community.aaa.sso.saml.storage;

import com.jivesoftware.community.impl.CachedPreparedStatement;
import com.jivesoftware.community.objecttype.JiveObjectResultFilter;
import com.jivesoftware.community.objecttype.impl.AbstractJiveObjectDAO;
import com.jivesoftware.util.SelectBuilder;
import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;
import org.springframework.dao.DataAccessException;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Date;

public class SamlAuthnRequestDAOImpl extends AbstractJiveObjectDAO<SamlAuthnRequest, JiveObjectResultFilter>
        implements SamlAuthnRequestDAO
{

    private static final Logger log = LogManager.getLogger(SamlAuthnRequestDAOImpl.class);

    public static final String TABLE_NAME = "jiveSamlAuthnRequest";
    public static final String PRIMARY_KEY_COLUMN_NAME = "msgID";
    public static final String COL_MESSAGE_XML = "messageXml";
    public static final String COL_CREATION_DATE = "creationDate";
    public static final String COL_REQUEST_ID = "requestID";

    private static final String SELECT_SQL = "SELECT * FROM " + TABLE_NAME + " WHERE requestID=?";
    private static final String DELETE_SQL = "DELETE FROM " + TABLE_NAME + " WHERE requestID=?";
    private static final String INSERT_SQL =
            "INSERT INTO " + TABLE_NAME +
                    "("
                    + PRIMARY_KEY_COLUMN_NAME
                    + "," + COL_REQUEST_ID
                    + "," + COL_MESSAGE_XML
                    + "," + COL_CREATION_DATE
                    + ")" + " VALUES " + "("
                    + ":" + PRIMARY_KEY_COLUMN_NAME
                    + ",:" + COL_REQUEST_ID
                    + ",:" + COL_MESSAGE_XML
                    + ",:" + COL_CREATION_DATE
                    + ")";
    private static final String DELETE_BY_DATE = "DELETE FROM " + TABLE_NAME + " WHERE " + COL_CREATION_DATE + " < ?";

    @Override
    protected String getTableName() {
        return TABLE_NAME;
    }

    @Override
    protected String getKeyColumnName() {
        return PRIMARY_KEY_COLUMN_NAME;
    }

    @Override
    protected int getObjectType() {
        return SamlAuthnRequestImpl.OBJECT_TYPE;
    }

    @Override
    protected void doInsert(SamlAuthnRequest msg, long id, Date creationDate) {
        getNamedParameterJdbcTemplate().update(INSERT_SQL, paramMap(msg, id, creationDate));
    }

    @Override
    @Transactional(readOnly = true, propagation = Propagation.SUPPORTS)
    public SamlAuthnRequest retrieveByRequestID(String requestID) {
        SamlAuthnRequest request = null;

        try {
            request = getJdbcTemplate().queryForObject(SELECT_SQL, getRowMapper(), requestID);
        }
        catch (DataAccessException e) {
            log.error("SAML AuthnRequest '" + requestID + "' could not be read from the database.", e);
        }

        return request;
    }

    @Override
    @Transactional(readOnly = true, propagation = Propagation.SUPPORTS)
    public int deleteByRequestID(String requestID) {
        try {
            return getJdbcTemplate().update(DELETE_SQL, requestID);
        }
        catch (DataAccessException e) {
            log.error("SAML AuthnRequest '" + requestID + "' could not be deleted from the database.", e);
        }
        return -1;
    }

    @Override
    @Transactional(readOnly = true, propagation = Propagation.SUPPORTS)
    public int deleteBeforeDate(Date date) {
        try {
            return getJdbcTemplate().update(DELETE_BY_DATE, date.getTime());
        }
        catch (DataAccessException e) {
            log.error("SamlAuthnRequests could not be deleted from the database before '" + date + "'.", e);
        }
        return -1;
    }

    @Override
    protected void doUpdate(SamlAuthnRequest app, Date modificationDate) {
        throw new UnsupportedOperationException("SAML AuthNRequests cannot be udpated");
    }

    @Override
    protected void addToSelectBuilder(CachedPreparedStatement preparedStatement, SelectBuilder selectBuilder,
            JiveObjectResultFilter resultFilter)
    {
        throw new UnsupportedOperationException("SAML AuthNRequests cannot be queried with ResultFilters");
    }

    @Override
    protected RowMapper<SamlAuthnRequest> getRowMapper() {
        return ROW_MAPPER;
    }

    private final RowMapper<SamlAuthnRequest> ROW_MAPPER = new ParameterizedRowMapper<SamlAuthnRequest>() {
        @Override
        public SamlAuthnRequest mapRow(ResultSet rs, int rowNum) throws SQLException {
            return new SamlAuthnRequestImpl(
                    rs.getLong(PRIMARY_KEY_COLUMN_NAME),
                    rs.getString(COL_REQUEST_ID),
                    rs.getString(COL_MESSAGE_XML),
                    new Date(rs.getLong(COL_CREATION_DATE)));
        }
    };

    private MapSqlParameterSource paramMap(SamlAuthnRequest msg, long id, Date modOrCreateDate) {
        MapSqlParameterSource paramMap = new MapSqlParameterSource();
        paramMap.addValue(PRIMARY_KEY_COLUMN_NAME, id);
        paramMap.addValue(COL_REQUEST_ID, msg.getRequestID());
        paramMap.addValue(COL_MESSAGE_XML, msg.getXmlString());
        paramMap.addValue(COL_CREATION_DATE, modOrCreateDate.getTime());
        return paramMap;
    }

}


